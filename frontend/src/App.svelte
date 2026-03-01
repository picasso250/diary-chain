<script>
  import { onMount } from "svelte";
  import { fade, slide } from "svelte/transition";
  import { ethers } from "ethers";
  import CryptoJS from "crypto-js";
  import { CONTRACT_ADDRESS, CONTRACT_ABI, TARGET_CHAIN_ID } from "./lib/constants";
  import { stringToColor } from "./lib/colors";

  let account = $state(null);
  let diaryContent = $state("");
  let allEntries = $state([]);
  let loading = $state(false);
  let isConnecting = $state(false);

  // 新功能状态
  let specialAttentionList = $state([]);
  let newAttentionAddress = $state("");
  let encryptionPassword = $state("");
  let showSettings = $state(false);

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
      alert("Please install a Web3 wallet (e.g., MetaMask).");
      return;
    }
    isConnecting = true;
    try {
      const isCorrectNetwork = await checkNetwork();
      if (!isCorrectNetwork) return;

      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      account = await signer.getAddress();
      
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
      
      await tx.wait();
      
      diaryContent = "";
      await fetchEntries();
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

  // 读取日志
  async function fetchEntries() {
    try {
      let provider;
      if (window.ethereum) {
        provider = new ethers.BrowserProvider(window.ethereum);
      } else {
        return; 
      }

      const contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, provider);
      const filter = contract.filters.EntryCreated();
      const logs = await contract.queryFilter(filter);

      const parsedLogs = logs.map(log => {
        return {
          user: log.args[0],
          timestamp: new Date(Number(log.args[1]) * 1000).toLocaleString(undefined, {
            year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
          }),
          content: log.args[2],
          blockNumber: log.blockNumber,
          hash: log.transactionHash
        };
      });

      allEntries = parsedLogs.reverse();
    } catch (error) {
      console.error("Fetch failed:", error);
    }
  }

  onMount(async () => {
    const saved = localStorage.getItem("specialAttention");
    if (saved) {
      try {
        specialAttentionList = JSON.parse(saved);
      } catch (e) {
        console.error("Failed to parse specialAttention", e);
      }
    }

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

<main class="min-h-screen bg-zinc-50 text-zinc-800 font-sans selection:bg-indigo-100 selection:text-indigo-900">
  <!-- Navbar -->
  <nav class="border-b border-zinc-200 p-4 sticky top-0 bg-white/80 backdrop-blur-md z-10 shadow-sm transition-all">
    <div class="max-w-4xl mx-auto flex justify-between items-center">
      <h1 class="text-xl font-semibold tracking-tight text-zinc-900 flex items-center gap-2">
        Diary Chain
        <span class="text-xs text-zinc-400 font-medium px-2 py-0.5 bg-zinc-100 rounded-full hidden sm:inline-block">
          Immutable Records
        </span>
      </h1>
      
      <button 
        onclick={connectWallet}
        class="text-sm px-5 py-2 rounded-lg bg-white border border-zinc-200 text-zinc-700 hover:border-indigo-300 hover:text-indigo-600 hover:shadow-sm hover:bg-indigo-50/50 transition-all duration-300 disabled:opacity-50 font-medium"
        disabled={isConnecting}
      >
        {#if account}
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-emerald-500"></div>
            {account.slice(0, 6)}...{account.slice(-4)}
          </div>
        {:else}
          {isConnecting ? 'Connecting...' : 'Connect Wallet'}
        {/if}
      </button>
    </div>
  </nav>

  <div class="max-w-4xl mx-auto p-4 pt-10 pb-20">
    
    <!-- Editor -->
    <section class="mb-12">
      <div class="bg-white p-6 md:p-8 rounded-2xl border border-zinc-200 shadow-sm hover:shadow-md transition-shadow duration-300 focus-within:ring-2 focus-within:ring-indigo-100 focus-within:border-indigo-300">
        <textarea
          bind:value={diaryContent}
          placeholder="What's on your mind today? Write an entry that lasts forever."
          class="w-full bg-transparent text-lg text-zinc-800 outline-none resize-none h-32 placeholder-zinc-400 custom-scrollbar leading-relaxed"
        ></textarea>

        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mt-6 border-t border-zinc-100 pt-5 gap-4">
          <div class="flex items-center gap-3 text-xs text-zinc-500 font-medium">
            <span class="flex items-center gap-1.5"><svg class="w-3.5 h-3.5 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg> Permanent</span>
            <span class="flex items-center gap-1.5"><svg class="w-3.5 h-3.5 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg> Public</span>
          </div>

          <button
            onclick={writeDiary}
            disabled={loading || !diaryContent.trim()}
            class="w-full sm:w-auto bg-indigo-600 text-white px-8 py-2.5 rounded-xl font-semibold shadow-sm shadow-indigo-200 hover:bg-indigo-700 hover:shadow transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed active:scale-[0.98] flex justify-center items-center gap-2"
          >
            {#if loading}
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              Publishing...
            {:else}
              Publish Entry
            {/if}
          </button>
        </div>
      </div>
    </section>

    <!-- Settings Toggle -->
    <div class="mb-4 flex justify-end">
      <button
        onclick={() => showSettings = !showSettings}
        class="text-sm font-medium text-zinc-500 hover:text-indigo-600 transition-colors flex items-center gap-1.5 px-3 py-1.5 rounded-lg hover:bg-zinc-100"
      >
        <svg class="w-4 h-4 transition-transform duration-300 {showSettings ? 'rotate-180' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
        Preferences
      </button>
    </div>

    {#if showSettings}
      <!-- Settings: Encryption & Attention -->
      <section transition:slide="{{ duration: 300 }}" class="mb-12 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white p-6 rounded-xl border border-zinc-200 shadow-sm">
          <h3 class="text-sm font-semibold text-zinc-800 mb-1 flex items-center gap-2">
            <svg class="w-4 h-4 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
            End-to-End Encryption
          </h3>
          <p class="text-xs text-zinc-500 mb-4">Set a password to encrypt new entries locally.</p>
          <input
            type="password"
            bind:value={encryptionPassword}
            placeholder="Your secret key"
            class="w-full bg-zinc-50 border border-zinc-200 p-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-400 transition-all"
          />
        </div>

        <div class="bg-white p-6 rounded-xl border border-zinc-200 shadow-sm">
          <h3 class="text-sm font-semibold text-zinc-800 mb-1 flex items-center gap-2">
            <svg class="w-4 h-4 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
            Watchlist
          </h3>
          <p class="text-xs text-zinc-500 mb-4">Filter timeline to specific addresses.</p>
          <div class="flex gap-2 mb-4">
            <input
              type="text"
              bind:value={newAttentionAddress}
              placeholder="0x..."
              class="flex-1 bg-zinc-50 border border-zinc-200 p-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-400 transition-all font-mono"
            />
            <button
              onclick={addAttention}
              class="px-4 py-2.5 bg-zinc-900 text-white rounded-lg text-sm font-medium hover:bg-zinc-800 transition-all"
            >
              Add
            </button>
          </div>

          {#if specialAttentionList.length > 0}
            <div class="space-y-2 max-h-32 overflow-y-auto pr-2 custom-scrollbar">
              {#each specialAttentionList as addr}
                <div class="flex justify-between items-center bg-zinc-50 p-2.5 rounded-lg border border-zinc-100 group">
                  <span class="font-mono text-xs text-zinc-600">{addr.slice(0, 10)}...{addr.slice(-8)}</span>
                  <button
                    onclick={() => removeAttention(addr)}
                    class="text-zinc-400 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
                    title="Remove"
                  >
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                  </button>
                </div>
              {/each}
            </div>
          {/if}
        </div>
      </section>
    {/if}

    <!-- Timeline -->
    <section class="space-y-6">
      <div class="flex items-center gap-4 mb-8">
        <h2 class="text-2xl font-bold text-zinc-900 tracking-tight">Timeline</h2>
      </div>

      {#if filteredEntries.length === 0}
        <div class="bg-white border border-zinc-100 rounded-2xl p-12 text-center shadow-sm">
          <div class="mx-auto w-12 h-12 bg-zinc-50 rounded-full flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-zinc-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
          </div>
          <h3 class="text-zinc-900 font-medium mb-1">No entries found</h3>
          <p class="text-zinc-500 text-sm">Be the first to leave a permanent record.</p>
        </div>
      {/if}

      <div class="space-y-6">
        {#each filteredEntries as entry (entry.hash)}
          <article transition:fade={{ duration: 400, delay: 50 }} class="bg-white rounded-2xl border border-zinc-200 shadow-sm hover:shadow-md hover:border-indigo-100 transition-all duration-300 overflow-hidden group">

            <header class="px-6 py-4 bg-zinc-50/50 border-b border-zinc-100 flex flex-wrap items-center justify-between gap-4">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs shadow-inner" style="background-color: {stringToColor(entry.user)}15; color: {stringToColor(entry.user)}; border: 1px solid {stringToColor(entry.user)}30;">
                  {entry.user.slice(2, 4).toUpperCase()}
                </div>
                <div>
                  <div class="font-mono text-xs font-medium text-zinc-700">
                    {entry.user.slice(0, 6)}...{entry.user.slice(-4)}
                  </div>
                  <div class="text-xs text-zinc-500 mt-0.5">{entry.timestamp}</div>
                </div>
              </div>

              <a
                href={`https://arbiscan.io/tx/${entry.hash}`}
                target="_blank"
                class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white border border-zinc-200 text-xs font-medium text-zinc-500 hover:text-indigo-600 hover:border-indigo-200 transition-colors"
              >
                <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                {entry.hash.slice(0, 6)}...{entry.hash.slice(-4)}
              </a>
            </header>

            <div class="px-6 py-5 prose prose-zinc max-w-none text-zinc-700">
              <p class="whitespace-pre-wrap leading-relaxed text-[15px]">
                {decryptContent(entry.content, encryptionPassword)}
              </p>
            </div>
          </article>
        {/each}
      </div>
    </section>
  </div>

  <footer class="mt-auto border-t border-zinc-200 bg-white py-8">
    <div class="max-w-4xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-zinc-500 font-medium">
      <div>© 2026 Diary Chain. Open Source.</div>
      <div class="flex gap-6">
        <a href={`https://arbiscan.io/address/${CONTRACT_ADDRESS}`} target="_blank" class="hover:text-indigo-600 transition-colors flex items-center gap-1"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg> Contract</a>
        <a href="https://github.com/picasso250/diary-chain" target="_blank" class="hover:text-zinc-900 transition-colors flex items-center gap-1"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"/></svg> GitHub</a>
      </div>
    </div>
  </footer>
</main>
