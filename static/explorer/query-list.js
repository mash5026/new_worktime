import{L as r}from"./index.js";import{t as d,g as u}from"./favorites.js";import{M as y}from"./main.js";function E(){const l=document.querySelector(".search");l&&l.focus()}function S(){document.querySelectorAll(".query_favorite_toggle").forEach(function(n){n.addEventListener("click",d)});let l={valueNames:["name"],handlers:{updated:[E]}};new r("queries",l),g()}function g(){let l=new y("#emailCsvModal",{}),n=null,a=function(e){return/^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i.test(e)},m=()=>{const e=document.getElementById("email-success-msg"),t=document.getElementById("email-error-msg");e.style.display="block",t.style.display="none",setTimeout(()=>l.hide(),2e3)},i=e=>{const t=document.getElementById("email-success-msg"),o=document.getElementById("email-error-msg");o.innerHTML=e,t.style.display="none",o.style.display="block"},c=function(e){let t=document.querySelector("#emailCsvInput").value,o="/"+n+"/email_csv?email="+t;a(t)?fetch(o,{method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":u()},body:JSON.stringify({email:t})}).then(s=>{if(!s.ok)throw new Error("Network response was not ok");return s.json()}).then(s=>{m()}).catch(s=>{i(s.message)}):i("Email is invalid")};document.querySelectorAll("#btnSubmitCsvEmail").forEach(function(e){e.addEventListener("click",c)}),document.querySelectorAll(".email-csv").forEach(e=>{e.addEventListener("click",function(t){t.preventDefault(),n=this.getAttribute("data-query-id"),l.show()})}),document.getElementById("emailCsvModal").addEventListener("hidden.bs.modal",e=>{document.getElementById("email-success-msg").style.display="none",document.getElementById("email-error-msg").style.display="none"})}export{S as setupQueryList};
