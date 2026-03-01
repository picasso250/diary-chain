with open('frontend/src/App.svelte', 'r') as f:
    lines = f.readlines()

with open('frontend/src/App.svelte', 'w') as f:
    for line in lines:
        if '><<button' in line:
            f.write(line.replace('><<button', '><button'))
        elif '><button' in line and '<button' in line.replace('><button', ''):
            # Try to fix double button
            pass
        else:
            f.write(line)
