// Usage: edit "courses" variable, go to udemy.com, press F12, paste this to console and run.


function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function sleep(ms) {
  return new Promise((resolve) => {
    return setTimeout(resolve, ms);
  });
}

async function buyall() {
  var courses = `3103916|DB0E783E9877F776F2BF
3173120|A65D1F313B9175C9A95F
3082522|ANNIVERSARYGIFT6
2918718|ANNIVERSARYGIFT10
3157052|ANNIVERSARYGIFT3
3156620|ANNIVERSARYGIFT2
3156426|ANNIVERSARYGIFT1
1386976|FREEJUNERF
2749466|3D96683DCFE648BD0F49
2702362|AE6541ADE6F4C270ED5A
543600|JUN2020FREE2
3030200|E76F3A3FB5D1A973B805
2605732|JUNEFIR2020
2579140|FREEBIE
1355712|00CF10F7EF2EB504CCDE
2405932|PLEASEENJOY108
776356|25C28ADF874BB5D5AD00
939930|060620_FREE
2619306|JUNFRE
3176900|DATA124
1832998|JUNEFREE
3115954|F66A302FB
1508164|MONGOPRACTICAL
1417860|SHARETHELOVE2020
2500506|32E514AC6C6C5E87F81C
2964096|WRITING90
3016358|CREATE-YOU-KEYLOGGER
3014480|DISCUDEMY.COM
3014478|DISCUDEMY.COM
3016366|ETHICALH1
2557320|DECORATORS-FREEBIES
3199916|05AEB4458E99DC26A65E
2497156|5517E7290B4227395E79
1971936|A115803A5A1155B0F5D1
2503534|JUNEFIR2020
927360|SHARETHELOVE2020
2120874|JUNEFIR2020
2996272|EXPERTEXCEL`;
//EDIT THIS

  courses = courses.split("\n");
  var courseindex;
  for (courseindex in courses) {
    var cid = courses[courseindex].split("|")[0];
    var coupon = courses[courseindex].split("|")[1];
    var presp = await fetch("https://www.udemy.com/payment/checkout-submit/", {
        "credentials": "include",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json;charset=utf-8",
            "X-Requested-With": "XMLHttpRequest",
            "Authorization": "Bearer "+getCookie("access_token"),
            "X-Udemy-Authorization": "Bearer "+getCookie("access_token"),
            "x-checkout-version": "2",
            "X-CSRFToken": getCookie("csrftoken"),
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        },
        "referrer": "https://www.udemy.com/",
        "body": "{\"checkout_environment\":\"Marketplace\",\"checkout_event\":\"Submit\",\"shopping_info\":{\"items\":[{\"discountInfo\":{\"code\":\""+coupon+"\"},\"price\":{\"amount\":0,\"currency\":\"TRY\"},\"buyable\":{\"id\":"+cid+",\"type\":\"course\"}}],\"is_cart\":true},\"payment_info\":{\"method_id\":\"0\",\"payment_vendor\":\"Free\",\"payment_method\":\"free-method\"},\"tax_info\":{\"tax_rate\":18,\"billing_location\":{\"country_code\":\"TR\",\"secondary_location_info\":null},\"currency_code\":\"try\",\"transaction_items\":[{\"tax_included_amount\":0,\"tax_excluded_amount\":0,\"tax_amount\":0,\"udemy_txn_item_reference\":\"course-"+cid+"\"}],\"tax_breakdown_type\":\"tax_inclusive\"}}",
        "method": "POST",
        "mode": "cors"
    });
    var prespjson = await presp.json();
    if((prespjson.detail ?? "").indexOf("available in ") > -1)
        await sleep(parseInt(prespjson.detail.split('available in ')[1].split(' seconds')[0]) * 1000);
    else
        await sleep(5000);
  }
}
buyall();
