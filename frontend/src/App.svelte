<script>
  import { onMount } from "svelte";
  import { ethers } from "ethers";
  import CryptoJS from "crypto-js";
  import { CONTRACT_ADDRESS, CONTRACT_ABI, TARGET_CHAIN_ID } from "./lib/constants";

  let account = $state(null);
  let diaryContent = $state("");
  let allEntries = $state([]);
  let loading = $state(false);
  let isConnecting = $state(false);

  // 新功能状态
  let specialAttentionList = $state([]);
  let newAttentionAddress = $state("");
  let encryptionPassword = $state("");

  // 响应式过滤
  let filteredEntries = $derived.by(() => {
    const myAddress = account?.toLowerCase();
    const attentionSet = new Set(specialAttentionList.map(a => a.toLowerCase()));

    return allEntries.filter(entry => {
      const user = entry.user.toLowerCase();
      return user === myAddress || attentionSet.has(user);
    });
  });

  // 检查并切换网络
  async function checkNetwork() {
    if (!window.ethereum) return;
    const chainId = await window.ethereum.request({ method: 'eth_chainId' });
    if (chainId !== TARGET_CHAIN_ID) {
      try {
        await window.ethereum.request({
          method: 'wallet_switchEthereumChain',
          params: [{ chainId: TARGET_CHAIN_ID }],
        });
        return true;
      } catch (switchError) {
        // 如果网络不存在（通常 Arbitrum 都在 MetaMask 默认列表中，但防万一），可以添加 wallet_addEthereumChain 逻辑
        console.error("Failed to switch network:", switchError);
        alert("Please switch your wallet to Arbitrum One network.");
        return false;
      }
    }
    return true;
  }

  // 连接钱包
  async function connectWallet() {
    if (!window.ethereum) {
      alert("Please install MetaMask!");
      return;
    }
    isConnecting = true;
    try {
      // 1. 先确保在正确的网络
      const isCorrectNetwork = await checkNetwork();
      if (!isCorrectNetwork) return;

      // 2. 获取账号
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      account = await signer.getAddress();
      
      // 3. 读取数据
      await fetchEntries();
    } catch (error) {
      console.error("Connection failed:", error);
    } finally {
      isConnecting = false;
    }
  }

  // 写入日记
  async function writeDiary() {
    if (!diaryContent.trim()) return;
    if (!account) {
      await connectWallet();
      if (!account) return;
    }

    loading = true;
    try {
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      const contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, signer);

      let contentToSend = diaryContent;
      if (encryptionPassword) {
        contentToSend = "AES:" + CryptoJS.AES.encrypt(diaryContent, encryptionPassword).toString();
      }

      const tx = await contract.writeEntry(contentToSend);
      console.log("Transaction sent:", tx.hash);
      
      // 等待交易确认
      await tx.wait();
      
      diaryContent = ""; // 清空输入框
      await fetchEntries(); // 刷新列表
    } catch (error) {
      console.error("Write failed:", error);
      alert("Failed to write to chain. See console for details.");
    } finally {
      loading = false;
    }
  }

  // 特别关注逻辑
  function addAttention() {
    if (!newAttentionAddress.trim()) return;
    if (!ethers.isAddress(newAttentionAddress)) {
      alert("Invalid Ethereum address");
      return;
    }
    const addr = newAttentionAddress.toLowerCase();
    if (!specialAttentionList.includes(addr)) {
      specialAttentionList = [...specialAttentionList, addr];
      localStorage.setItem("specialAttention", JSON.stringify(specialAttentionList));
      fetchEntries();
    }
    newAttentionAddress = "";
  }

  function removeAttention(addr) {
    specialAttentionList = specialAttentionList.filter(a => a !== addr);
    localStorage.setItem("specialAttention", JSON.stringify(specialAttentionList));
    fetchEntries();
  }

  // 解密逻辑
  function decryptContent(content, password) {
    if (!content.startsWith("AES:")) return content;
    if (!password) return "[Encrypted Content]";
    try {
      const bytes = CryptoJS.AES.decrypt(content.slice(4), password);
      const decrypted = bytes.toString(CryptoJS.enc.Utf8);
      if (!decrypted) return "[Decryption Failed]";
      return decrypted;
    } catch (e) {
      return "[Decryption Error]";
    }
  }

  // 读取日志 (从区块链事件中)
  async function fetchEntries() {
    try {
      // 如果已连接钱包用 BrowserProvider，否则用只读的 JsonRpcProvider (这里为了简单统一用 BrowserProvider，实际生产可用 Alchemy/Infura)
      let provider;
      if (window.ethereum) {
        provider = new ethers.BrowserProvider(window.ethereum);
      } else {
        // Fallback for read-only if no wallet (optional)
        return; 
      }

      const contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, provider);
      
      // 查询所有 EntryCreated 事件
      // queryFilter(event, fromBlock, toBlock)
      // 实际生产中应限制 block range 或使用 Graph，这里本地测试查所有
      const filter = contract.filters.EntryCreated();
      const logs = await contract.queryFilter(filter);

      // 解析日志
      const parsedLogs = logs.map(log => {
        // log.args 包含: [user, timestamp, content]
        return {
          user: log.args[0],
          timestamp: new Date(Number(log.args[1]) * 1000).toLocaleString(),
          content: log.args[2],
          blockNumber: log.blockNumber,
          hash: log.transactionHash
        };
      });

      // 按时间倒序排列 (最新的在最前)
      allEntries = parsedLogs.reverse();
    } catch (error) {
      console.error("Fetch failed:", error);
    }
  }

  onMount(async () => {
    // 加载特别关注列表
    const saved = localStorage.getItem("specialAttention");
    if (saved) {
      try {
        specialAttentionList = JSON.parse(saved);
      } catch (e) {
        console.error("Failed to parse specialAttention", e);
      }
    }

    // 尝试自动读取（如果用户之前授权过，或者只读模式）
    if (window.ethereum) {
       try {
         const provider = new ethers.BrowserProvider(window.ethereum);
         const accounts = await provider.listAccounts();
         if (accounts.length > 0) {
           account = await accounts[0].getAddress();
         }
       } catch (e) {
         console.warn("Failed to get initial account", e);
       }

       // 监听账号切换
       window.ethereum.on('accountsChanged', (accounts) => {
         if (accounts.length > 0) {
           account = accounts[0];
         } else {
           account = null;
         }
         fetchEntries();
       });
       fetchEntries();
    }
  });
</script>

<main class="min-h-screen bg-stone-900 text-stone-200 font-mono selection:bg-red-900 selection:text-white">
  <!-- Navbar -->
  <nav class="border-b border-stone-800 p-4 sticky top-0 bg-stone-900/95 backdrop-blur z-10">
    <div class="max-w-3xl mx-auto flex justify-between items-center">
      <h1 class="text-xl font-bold tracking-tighter text-red-500 uppercase">
        Diary Chain
        <span class="text-xs text-stone-500 font-normal normal-case block sm:inline sm:ml-2">
          // Anti-Revisionism Protocol
        </span>
      </h1>
      
      <button 
        onclick={connectWallet}
        class="text-sm px-4 py-2 border border-stone-700 hover:border-red-500 hover:text-red-500 transition-colors duration-300 disabled:opacity-50"
        disabled={isConnecting}
      >
        {#if account}
          {account.slice(0, 6)}...{account.slice(-4)}
        {:else}
          {isConnecting ? 'Connecting...' : 'Connect Wallet'}
        {/if}
      </button>
    </div>
  </nav>

  <div class="max-w-3xl mx-auto p-4 pt-8">
    
    <!-- Editor -->
    <section class="mb-12">
      <div class="relative group">
        <div class="absolute -inset-0.5 bg-gradient-to-r from-red-900 to-stone-800 rounded opacity-30 group-hover:opacity-70 transition duration-500 blur"></div>
        <div class="relative bg-stone-950 p-6 rounded border border-stone-800">
          <textarea
            bind:value={diaryContent}
            placeholder="Record history as it happens. No edits. No deletions."
            class="w-full bg-transparent text-lg outline-none resize-none h-32 placeholder-stone-600"
          ></textarea>
          <div class="flex justify-between items-center mt-4 border-t border-stone-900 pt-4">
            <span class="text-xs text-stone-500">
              Immutable • Permanent • Public
            </span>
            <button 
              onclick={writeDiary}
              disabled={loading || !diaryContent.trim()}
              class="bg-stone-100 text-stone-900 hover:bg-red-600 hover:text-white px-6 py-2 font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Engraving...' : 'ENGRAVE'}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Settings: Encryption & Attention -->
    <section class="mb-12 grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-stone-950 p-6 rounded border border-stone-800">
        <h3 class="text-sm font-bold text-red-500 uppercase mb-4 tracking-widest">Encryption</h3>
        <input
          type="password"
          bind:value={encryptionPassword}
          placeholder="Set Encryption Password"
          class="w-full bg-stone-900 border border-stone-800 p-2 text-sm outline-none focus:border-red-500 transition-colors"
        />
        <p class="text-[10px] text-stone-600 mt-2 italic">
          If set, new diaries will be encrypted. You must use the SAME password to decrypt them later.
        </p>
      </div>

      <div class="bg-stone-950 p-6 rounded border border-stone-800">
        <h3 class="text-sm font-bold text-red-500 uppercase mb-4 tracking-widest">Special Attention</h3>
        <div class="flex gap-2 mb-4">
          <input
            type="text"
            bind:value={newAttentionAddress}
            placeholder="Address (0x...)"
            class="flex-1 bg-stone-900 border border-stone-800 p-2 text-xs outline-none focus:border-red-500 transition-colors"
          />
          <button
            onclick={addAttention}
            class="px-4 py-2 bg-stone-100 text-stone-900 text-xs font-bold hover:bg-red-600 hover:text-white transition-all"
          >
            ADD
          </button>
        </div>

        <div class="space-y-2 max-h-32 overflow-y-auto pr-2 custom-scrollbar">
          {#each specialAttentionList as addr}
            <div class="flex justify-between items-center text-[10px] bg-stone-900 p-2 border border-stone-800">
              <span class="font-mono">{addr.slice(0, 10)}...{addr.slice(-8)}</span>
              <button
                onclick={() => removeAttention(addr)}
                class="text-red-500 hover:text-red-400 font-bold"
              >
                REMOVE
              </button>
            </div>
          {/each}
        </div>
      </div>
    </section>

    <!-- Timeline -->
    <section class="space-y-8">
      <div class="flex items-center gap-4">
        <h2 class="text-2xl font-bold text-stone-100">Chronicle</h2>
        <div class="h-px bg-stone-800 flex-1"></div>
      </div>

      {#if filteredEntries.length === 0}
        <div class="text-center py-12 text-stone-600 italic">
          The chain is silent. Be the first to speak.
        </div>
      {/if}

      {#each filteredEntries as entry (entry.hash)}
        <article class="pl-4 border-l-2 border-stone-800 hover:border-red-900 transition-colors duration-300 relative">
          <!-- Dot -->
          <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-stone-900 border-2 border-stone-800"></div>
          
          <header class="mb-2 flex flex-wrap items-baseline gap-x-3 text-xs text-stone-500">
            <span class="text-red-400 font-bold">{entry.timestamp}</span>
            <span class="font-mono">{entry.user.slice(0, 6)}...{entry.user.slice(-4)}</span>
            <a 
              href={`https://arbiscan.io/tx/${entry.hash}`} 
              target="_blank" 
              class="hover:text-stone-300 hover:underline decoration-stone-700"
            >
              {entry.hash.slice(0, 6)}...{entry.hash.slice(-4)}
            </a>
          </header>
          
          <div class="prose prose-invert prose-stone max-w-none">
            <p class="whitespace-pre-wrap leading-relaxed text-stone-300">
              {decryptContent(entry.content, encryptionPassword)}
            </p>
          </div>
        </article>
      {/each}
    </section>
  </div>

  <footer class="max-w-3xl mx-auto p-4 py-8 border-t border-stone-800 flex justify-between items-center text-xs text-stone-600">
    <div>© 2025 Diary Chain</div>
    <a href="https://github.com/picasso250/diary-chain" target="_blank" class="hover:text-stone-400 underline decoration-stone-800">GitHub</a>
  </footer>
</main>