import re

with open('frontend/src/App.svelte', 'r') as f:
    content = f.read()

# Make the textarea look better when focused
content = re.sub(
    r'<div class="relative bg-stone-950 p-6 rounded border border-stone-800">',
    r'<div class="relative bg-stone-950 p-6 rounded border border-stone-800 focus-within:border-stone-600 transition-colors">',
    content
)

# Apply slide transition to settings block
content = re.sub(
    r'<!-- Settings: Encryption & Attention -->\n\s*<section class="mb-12 grid grid-cols-1 md:grid-cols-2 gap-6">',
    r'<!-- Settings: Encryption & Attention -->\n      <section transition:slide="{{ duration: 300 }}" class="mb-12 grid grid-cols-1 md:grid-cols-2 gap-6">',
    content
)

# Apply fade transition to entries
content = re.sub(
    r'<article class="pl-4 border-l-2 border-stone-800 hover:border-red-900 transition-colors duration-300 relative">',
    r'<article transition:fade={{ duration: 400, delay: 100 }} class="pl-8 py-2 ml-2 border-l-2 border-stone-800 hover:border-red-500/50 transition-colors duration-500 relative group">',
    content
)

# Change the dot style on hover and address color
content = re.sub(
    r'<!-- Dot -->\n\s*<div class="absolute -left-\[9px\] top-0 w-4 h-4 rounded-full bg-stone-900 border-2 border-stone-800"><\/div>',
    r'<!-- Dot -->\n          <div class="absolute -left-[11px] top-[14px] w-5 h-5 rounded-full bg-stone-900 border-[3px] border-stone-800 group-hover:border-red-500 group-hover:bg-red-900 group-hover:scale-110 transition-all duration-300 shadow-[0_0_0_4px_rgba(28,25,23,1)]"></div>',
    content
)

content = re.sub(
    r'<span class="font-mono">{entry.user.slice\(0, 6\)}\.\.\.{entry.user.slice\(-4\)}</span>',
    r'<span class="font-mono px-2 py-0.5 rounded bg-stone-900/50 border border-stone-800 group-hover:border-stone-600 transition-colors" style="color: {stringToColor(entry.user)}">{entry.user.slice(0, 6)}...{entry.user.slice(-4)}</span>',
    content
)

# Enhance the navbar
content = re.sub(
    r'<nav class="border-b border-stone-800 p-4 sticky top-0 bg-stone-900/95 backdrop-blur z-10">',
    r'<nav class="border-b border-stone-800 p-4 sticky top-0 bg-stone-900/80 backdrop-blur-md z-10 shadow-sm">',
    content
)

content = re.sub(
    r'<button \n        onclick={connectWallet}\n        class="text-sm px-4 py-2 border border-stone-700 hover:border-red-500 hover:text-red-500 transition-colors duration-300 disabled:opacity-50"\n        disabled={isConnecting}\n      >',
    r'<button \n        onclick={connectWallet}\n        class="text-sm px-5 py-2 rounded border border-stone-700 hover:border-red-500 hover:bg-red-500/10 hover:text-red-500 transition-all duration-300 disabled:opacity-50 font-bold tracking-wider"\n        disabled={isConnecting}\n      >',
    content
)

content = re.sub(
    r'<div class="absolute -inset-0\.5 bg-gradient-to-r from-red-900 to-stone-800 rounded opacity-30 group-hover:opacity-70 transition duration-500 blur"><\/div>',
    r'<div class="absolute -inset-1 bg-gradient-to-r from-red-900 via-stone-800 to-red-900 rounded opacity-20 group-hover:opacity-60 transition duration-1000 blur-lg"></div>',
    content
)

content = re.sub(
    r'<button \n              onclick={writeDiary}\n              disabled={loading \|\| !diaryContent.trim\(\)}\n              class="bg-stone-100 text-stone-900 hover:bg-red-600 hover:text-white px-6 py-2 font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed"\n            >',
    r'<button \n              onclick={writeDiary}\n              disabled={loading || !diaryContent.trim()}\n              class="bg-stone-100 text-stone-900 hover:bg-red-600 hover:text-white px-8 py-2.5 rounded font-bold tracking-widest transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-[0_0_15px_rgba(220,38,38,0.5)] active:scale-95"\n            >',
    content
)

# Add hover styles to the content div for readability
content = re.sub(
    r'<div class="prose prose-invert prose-stone max-w-none">',
    r'<div class="prose prose-invert prose-stone max-w-none bg-stone-900/40 p-5 rounded-lg border border-stone-800/50 group-hover:border-stone-700/80 group-hover:bg-stone-900/60 transition-all duration-300">',
    content
)

content = re.sub(
    r'<textarea\n            bind:value={diaryContent}\n            placeholder="Record history as it happens. No edits. No deletions."\n            class="w-full bg-transparent text-lg outline-none resize-none h-32 placeholder-stone-600"\n          ><\/textarea>',
    r'<textarea\n            bind:value={diaryContent}\n            placeholder="Record history as it happens. No edits. No deletions."\n            class="w-full bg-transparent text-lg outline-none resize-none h-36 placeholder-stone-600 custom-scrollbar"\n          ></textarea>',
    content
)

with open('frontend/src/App.svelte', 'w') as f:
    f.write(content)
