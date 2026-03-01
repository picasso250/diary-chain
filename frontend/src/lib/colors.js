export function stringToColor(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  let color = '#';
  for (let i = 0; i < 3; i++) {
    const value = (hash >> (i * 8)) & 0xFF;
    // Keep it relatively balanced for a light/professional theme
    const adjusted = Math.max(80, Math.min(200, value)).toString(16);
    color += ('00' + adjusted).slice(-2);
  }
  return color;
}
