import re

with open('frontend/src/App.svelte', 'r') as f:
    content = f.read()

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
