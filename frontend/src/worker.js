export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.endsWith("/index.html")) {
      const directoryPath = url.pathname.slice(0, -"/index.html".length);
      url.pathname = directoryPath ? `${directoryPath}/` : "/";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
