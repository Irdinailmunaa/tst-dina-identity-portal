const TOKEN_KEY="tst_token";
const getToken=()=>localStorage.getItem(TOKEN_KEY);
const setToken=t=>{ if(t) localStorage.setItem(TOKEN_KEY,t); refreshToken(); };
const clearToken=()=>{ localStorage.removeItem(TOKEN_KEY); refreshToken(); };

function refreshToken(){
  const t=getToken();
  const el=document.getElementById("tokenPreview");
  if(!t) el.textContent="-";
  else el.textContent=t.length>24?(t.slice(0,12)+"..."+t.slice(-8)):t;
}

async function api(method,path,body=null){
  const headers={"content-type":"application/json"};
  const token=getToken();
  if(token) headers["authorization"]=`Bearer ${token}`;
  const res=await fetch(path,{method,headers,body:body?JSON.stringify(body):null});
  const text=await res.text();
  let data; try{data=JSON.parse(text);}catch{data=text;}
  return {ok:res.ok,status:res.status,data};
}
const show=(id,obj)=>document.getElementById(id).textContent=typeof obj==="string"?obj:JSON.stringify(obj,null,2);

document.getElementById("btnRegister").addEventListener("click", async()=>{
  const username=document.getElementById("regUser").value.trim();
  const password=document.getElementById("regPass").value;
  const role=document.getElementById("regRole").value;
  show("regOut", await api("POST","/api/auth/register",{username,password,role}));
});

document.getElementById("btnLogin").addEventListener("click", async()=>{
  const username=document.getElementById("logUser").value.trim();
  const password=document.getElementById("logPass").value;
  const r=await api("POST","/api/auth/login",{username,password});
  show("logOut", r);
  if(r.ok){
    const token=r.data.access_token||r.data.token||r.data.jwt;
    if(token) setToken(token);
  }
});

document.getElementById("btnMe").addEventListener("click", async()=>show("meOut", await api("GET","/api/auth/me")));
document.getElementById("btnLogout").addEventListener("click", async()=>{clearToken(); show("meOut",{ok:true,message:"token cleared"})});

document.getElementById("btnAttendance").addEventListener("click", async()=>{
  const eid=document.getElementById("attEvent").value.trim();
  show("attOut", await api("GET",`/api/attendance/${encodeURIComponent(eid)}`));
});

document.getElementById("btnCheckin").addEventListener("click", async()=>{
  const event_id=document.getElementById("attEvent").value.trim();
  const ticket_id=document.getElementById("ciTicket").value.trim();
  show("ciOut", await api("POST","/api/checkins",{event_id,ticket_id}));
});

refreshToken();

