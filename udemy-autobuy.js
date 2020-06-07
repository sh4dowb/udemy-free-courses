// Usage: edit "courses" variable, go to udemy.com, press F12, paste this to console and run.
// todo: parse rate limiting and wait accordingly, add course and coupons in 1 request


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
  var courses = `3175938|FIBUREWE
3072680|9139BEF7971B6A165886`;
//EDIT THIS

  courses = courses.split("\n");
  var courseindex;
  for (courseindex in courses) {
    var cid = courses[courseindex].split("|")[0];
    var coupon = courses[courseindex].split("|")[1];
    const twitterResponse = await fetch("https://www.udemy.com/api-2.0/shopping-carts/me/", {
      "credentials" : "include",
      "headers" : {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Accept" : "application/json, text/plain, */*",
        "Accept-Language" : "en-US,en;q=0.5",
        "Content-Type" : "application/json;charset=utf-8",
        "X-Requested-With" : "XMLHttpRequest",
        "Authorization" : "Bearer " + getCookie("access_token"),
        "X-Udemy-Authorization" : "Bearer " + getCookie("access_token"),
        "Pragma" : "no-cache",
        "Cache-Control" : "no-cache"
      },
      "referrer" : "https://www.udemy.com/",
      "mode" : "cors"
    });
    var etag = twitterResponse.headers.get("etag");
    await fetch("https://www.udemy.com/api-2.0/shopping-carts/me/cart/", {
      "credentials" : "include",
      "headers" : {
        "Accept" : "application/json, text/plain, */*",
        "Accept-Language" : "en-US,en;q=0.5",
        "Content-Type" : "application/json;charset=utf-8",
        "X-Requested-With" : "XMLHttpRequest",
        "Authorization" : "Bearer " + getCookie("access_token"),
        "X-Udemy-Authorization" : "Bearer " + getCookie("access_token"),
        "Pragma" : "no-cache",
        "If-Match" : etag,
        "Cache-Control" : "no-cache"
      },
      "referrer" : "https://www.udemy.com/",
      "body" : '{"buyables":[{"buyable_object_type":"course","id":' + cid + ',"buyable_context":{}}]}',
      "method" : "POST",
      "mode" : "cors"
    });
    await sleep(500);
    const resp = await fetch("https://www.udemy.com/api-2.0/shopping-carts/me/discounts/", {
      "credentials" : "include",
      "headers" : {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Accept" : "application/json, text/plain, */*",
        "Accept-Language" : "en-US,en;q=0.5",
        "Content-Type" : "application/json;charset=utf-8",
        "X-Requested-With" : "XMLHttpRequest",
        "Authorization" : "Bearer " + getCookie("access_token"),
        "X-Udemy-Authorization" : "Bearer " + getCookie("access_token"),
        "Pragma" : "no-cache",
        "If-Match" : etag,
        "Cache-Control" : "no-cache"
      },
      "referrer" : "https://www.udemy.com/",
      "body" : '{"codes":["' + coupon + '"]}',
      "method" : "POST",
      "mode" : "cors"
    });
    respjson = await resp.json();
    await sleep(500);
    if (respjson.cart.length > 0) {
      await fetch("https://www.udemy.com/payment/checkout-submit/", {
        "credentials" : "include",
        "headers" : {
          "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0",
          "Accept" : "application/json, text/plain, */*",
          "Accept-Language" : "en-US,en;q=0.5",
          "Content-Type" : "application/json;charset=utf-8",
          "X-Requested-With" : "XMLHttpRequest",
          "Authorization" : "Bearer " + getCookie("access_token"),
          "X-Udemy-Authorization" : "Bearer " + getCookie("access_token"),
          "x-checkout-version" : "2",
          "X-CSRFToken" : getCookie("csrftoken"),
          "Pragma" : "no-cache",
          "If-Match" : etag,
          "Cache-Control" : "no-cache"
        },
        "referrer" : "https://www.udemy.com/cart/checkout/",
        "body" : '{"checkout_event":"Submit","shopping_cart":{"items":[{"discountInfo":{"code":"' + coupon + '"},"purchasePrice":{"amount":0,"currency":"USD","price_string":"Free","currency_symbol":"$"},"buyableType":"course","buyableId":"' + cid + '","buyableContext":{}}],"is_cart":true},"payment_info":{"payment_vendor":"Free","payment_method":"free-method"},"tax_info":{"is_tax_enabled":true,"tax_rate":"7.700","billing_location":{"country_code":"CH","secondary_location_info":null},"currency_code":"usd","transaction_items":[{"udemy_txn_item_reference":"course-' + 
        cid + '","tax_amount":"0.00","tax_included_amount":"0","tax_excluded_amount":"0.00"}],"tax_breakdown_type":"tax_inclusive"}}',
        "method" : "POST",
        "mode" : "cors"
      });
    }
    await sleep(2000);
  }
}
buyall();
