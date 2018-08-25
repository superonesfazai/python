
        chrome.proxy.settings.set({
            value: {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "127.0.0.1/?types=0",
                        port: 8000
                    },
                    bypassList: ["foobar.com"]
                }
            },
            scope: "regular"
        }, function() {});

        chrome.webRequest.onAuthRequired.addListener(
            function (details) {
                return {
                    authCredentials: {
                        username: "",
                        password: ""
                    }
                };
            },
            { urls: ["<all_urls>"] },
            [ 'blocking' ]
        );
        