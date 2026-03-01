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
    r'<article transition:fade="{{ duration: 400 }}" class="pl-5 py-2 border-l-2 border-stone-800 hover:border-stone-500 transition-colors duration-300 relative group">',
    content
)

# Change the dot style on hover and address color
content = re.sub(
    r'<!-- Dot -->\n\s*<div class="absolute -left-\[9px\] top-0 w-4 h-4 rounded-full bg-stone-900 border-2 border-stone-800"></div>',
    r'<!-- Dot -->\n          <div class="absolute -left-[11px] top-3 w-5 h-5 rounded-full bg-stone-900 border-2 border-stone-800 group-hover:border-stone-500 group-hover:scale-110 transition-all duration-300"></div>',
    content
)

content = re.sub(
    r'<span class="font-mono">{entry.user.slice\(0, 6\)}\.\.\.{entry.user.slice\(-4\)}</span>',
    r'<span class="font-mono px-2 py-0.5 rounded bg-stone-900/50 border border-stone-800 group-hover:border-stone-600 transition-colors" style="color: {stringToColor(entry.user)}">{entry.user.slice(0, 6)}...{entry.user.slice(-4)}</span>',
    content
)

with open('frontend/src/App.svelte', 'w') as f:
    f.write(content)
