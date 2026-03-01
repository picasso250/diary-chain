export function stringToColor(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  let color = '#';
  for (let i = 0; i < 3; i++) {
    const value = (hash >> (i * 8)) & 0xFF;
    // Keep it relatively light/pastel so it's readable on dark mode
    const adjusted = Math.max(120, value).toString(16);
    color += ('00' + adjusted).slice(-2);
  }
  return color;
}
