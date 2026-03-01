import re

with open('frontend/src/App.svelte', 'r') as f:
    content = f.read()

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
    r'<div class="relative group">\n\s*<div class="absolute -inset-0\.5 bg-gradient-to-r from-red-900 to-stone-800 rounded opacity-30 group-hover:opacity-70 transition duration-500 blur"><\/div>',
    r'<div class="relative group">\n        <div class="absolute -inset-1 bg-gradient-to-r from-red-900 via-stone-800 to-red-900 rounded opacity-20 group-hover:opacity-60 transition duration-1000 blur-lg"></div>',
    content
)

content = re.sub(
    r'<button \n              onclick={writeDiary}\n              disabled={loading || !diaryContent\.trim\(\)}\n              class="bg-stone-100 text-stone-900 hover:bg-red-600 hover:text-white px-6 py-2 font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed"\n            >',
    r'<button \n              onclick={writeDiary}\n              disabled={loading || !diaryContent.trim()}\n              class="bg-stone-100 text-stone-900 hover:bg-red-600 hover:text-white px-8 py-2.5 rounded font-bold tracking-widest transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-[0_0_15px_rgba(220,38,38,0.5)] active:scale-95"\n            >',
    content
)

content = re.sub(
    r'<div class="absolute -left-\[11px\] top-3 w-5 h-5 rounded-full bg-stone-900 border-2 border-stone-800 group-hover:border-stone-500 group-hover:scale-110 transition-all duration-300"><\/div>',
    r'<!-- Dot -->\n          <div class="absolute -left-[11px] top-[14px] w-5 h-5 rounded-full bg-stone-900 border-[3px] border-stone-800 group-hover:border-red-500 group-hover:bg-red-900 group-hover:scale-110 transition-all duration-300 shadow-[0_0_0_4px_rgba(28,25,23,1)]"></div>',
    content
)

content = re.sub(
    r'<article transition:fade="{{ duration: 400 }}" class="pl-5 py-2 border-l-2 border-stone-800 hover:border-stone-500 transition-colors duration-300 relative group">',
    r'<article transition:fade={{ duration: 400, delay: 100 }} class="pl-8 py-2 ml-2 border-l-2 border-stone-800 hover:border-red-500/50 transition-colors duration-500 relative group">',
    content
)

with open('frontend/src/App.svelte', 'w') as f:
    f.write(content)
