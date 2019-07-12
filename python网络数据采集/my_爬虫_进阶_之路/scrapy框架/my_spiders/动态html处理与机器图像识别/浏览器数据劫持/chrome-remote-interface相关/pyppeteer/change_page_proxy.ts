// import {Frame, Page, Request, Response, SetCookie} from "puppeteer";
// import {DownloadUtil} from "../common/util/DownloadUtil";
// import {logger} from "../common/util/logger";
// import {FileUtil} from "../common/util/FileUtil";
// import * as http from "http";
// import {RequestUtil} from "..";
//
// /**
//  * 页面使用单独的proxy
//  * @param page
//  * @param proxy 代理服务器地址，例如：http://127.0.0.1:2007
//  * @param enableCache 代理请求的过程中是否启用缓存
//  */
// static async useProxy(page: Page, proxy: string, enableCache: boolean=true) {
//     page["_proxy"] = proxy;
//     page["_enableCacheInProxy"] = enableCache;
//     await page.setRequestInterception(true);
//     if (!page["_proxyHandler"]) {
//         const _proxyHandler = async (req: Request) => {
//             const proxy = page["_proxy"];
//             const enableCache = page["_enableCacheInProxy"];
//
//             if (req["_interceptionHandled"] || !req["_allowInterception"]) {
//                 return;
//             }
//             else if (proxy && req.url().startsWith("http")) {
//                 if (!req.isNavigationRequest()) {
//                     // nav请求始终不缓存
//                     const responseCache = enableCache ? await page.evaluate(url => {
//                         const cache = localStorage.getItem(url);
//                         if (cache) {
//                             if (parseInt(cache.substring(0, cache.indexOf("\n"))) <= new Date().getTime()) {
//                                 // 已过期
//                                 localStorage.removeItem(url);
//                             }
//                             else {
//                                 return cache;
//                             }
//                         }
//                     }, req.url()).catch(err => {}) : null;
//                     if (responseCache) {
//                         let [expires, statusCodeStr, bodyBase64] = responseCache.split("\n");
//                         const statusCode = +statusCodeStr;
//                         const body = Buffer.from(bodyBase64, "base64");
//                         await req.respond({
//                             status: statusCode,
//                             headers: {
//                                 cache: "from-local-storage"
//                             },
//                             body: body
//                         });
//                         return;
//                     }
//                 }
//
//                 const options = {
//                     url: req.url(),
//                     method: req.method(),
//                     headers: req.headers(),
//                     body: req.postData(),
//                     proxy: proxy
//                 };
//
//                 try {
//                     if (options.headers && (options.headers.cookie == null || options.headers.Cookie == null)) {
//                         // 设置cookie
//                         const cookies = await page.cookies(options.url);
//                         if (cookies.length) {
//                             // console.log(options.url + "\n"
//                             //     + cookies.map(item => item.name + "=" + item.value + "; domain=" + item.domain).join("\n") + "\n");
//                             options.headers.cookie = cookies.map(item =>
//                                 item.name + "=" + item.value).join("; ");
//                         }
//                     }
//                     const proxyRes = await RequestUtil.simple(options);
//                     const headers = proxyRes.headers;
//                     // 处理返回结果的 header；主要是处理 set-cookie
//                     for (let name in headers) {
//                         const value = headers[name];
//
//                         if (name == "set-cookie") {
//                             if (value.length == 0) {
//                                 headers[name] = ("" + value[0]) as any;
//                             }
//                             else {
//                                 const setCookies: SetCookie[] = [];
//                                 for (let item of value) {
//                                     const setCookie: SetCookie = {
//                                         name: null,
//                                         value: null
//                                     };
//                                     item.split("; ").forEach((keyVal, keyValI) => {
//                                         const eqI = keyVal.indexOf("=");
//                                         let key;
//                                         let value;
//                                         if (eqI > -1) {
//                                             key = keyVal.substring(0, eqI);
//                                             value = keyVal.substring(eqI + 1);
//                                         }
//                                         else {
//                                             key = keyVal;
//                                             value = "";
//                                         }
//                                         const lowerKey = key.toLowerCase();
//
//                                         if (keyValI == 0) {
//                                             setCookie.name = key;
//                                             setCookie.value = value;
//                                         }
//                                         else if (lowerKey == "expires") {
//                                             const expires = new Date(value).getTime();
//                                             if (!isNaN(expires)) {
//                                                 setCookie.expires = +(expires / 1000).toFixed(0);
//                                             }
//                                         }
//                                         else if (lowerKey == "max-age") {
//                                             if (!setCookie.expires) {
//                                                 const expires = +value;
//                                                 if (!isNaN(expires)) {
//                                                     setCookie.expires = expires;
//                                                 }
//                                             }
//                                         }
//                                         else if (lowerKey == "path" || key == "domain") {
//                                             setCookie[lowerKey] = value;
//                                         }
//                                         else if (lowerKey == "samesite") {
//                                             setCookie.httpOnly = true;
//                                         }
//                                         else if (lowerKey == "httponly") {
//                                             setCookie.httpOnly = true;
//                                         }
//                                         else if (lowerKey == "secure") {
//                                             setCookie.secure = true;
//                                         }
//                                     });
//                                     headers["set-cookie-" + setCookies.length] = item;
//                                     setCookies.push(setCookie);
//                                 }
//                                 await page.setCookie(...setCookies).catch(err => {});
//                                 delete headers[name];
//                             }
//                         }
//                         else if (typeof value != "string") {
//                             if (value instanceof Array) {
//                                 headers[name] = JSON.stringify(value);
//                             }
//                             else {
//                                 headers[name] = "" + value;
//                             }
//                         }
//                     }
//
//                     if (!req.isNavigationRequest()) {
//                         // nav请求始终不缓存
//                         //  如果有 Expires ，则保存缓存
//                         const expires = new Date(headers.expires || headers.Expires as string).getTime();
//                         if (enableCache && expires > new Date().getTime()) {
//                             const bodyBase64 = proxyRes.body.toString("base64");
//                             const responseCache = `${expires}\n${proxyRes.status}\n${bodyBase64}`;
//                             await page.evaluate((url, responseCache) => {
//                                 localStorage.setItem(url, responseCache);
//                             }, req.url(), responseCache).catch(err => {});
//                         }
//                     }
//
//                     await req.respond(proxyRes as any).catch(err => {});
//                 }
//                 catch(err) {
//                     await req.abort("failed").catch(err => {});
//                 }
//             }
//         };
//         page.on("request", _proxyHandler);
//     }
// }
