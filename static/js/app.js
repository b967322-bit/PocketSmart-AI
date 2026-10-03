async function logout(){await fetch("/logout",{method:"POST"});location.href="/";}
document.addEventListener("submit",async(event)=>{
 const form=event.target;if(form.id!=="planner-form")return;event.preventDefault();
 const planner=location.pathname.split("/").pop(),message=document.getElementById("message");message.textContent="Generating your plan...";
 let payload,endpoint;
 if(planner==="home"){
   const fd=new FormData(form),items={};
   (fd.get("items_text")||"").split(",").map(x=>x.trim()).filter(Boolean).forEach(x=>{const [k,v]=x.split(":").map(y=>y.trim());items[k]=Number(v||1)});
   payload={budget:Number(fd.get("budget")),city:fd.get("city"),rooms:(fd.get("rooms_text")||"").split(",").map(x=>x.trim()).filter(Boolean),style:fd.get("style"),items};endpoint="/generate-home";
 } else if(planner==="party"){
   const fd=new FormData(form);payload={budget:Number(fd.get("budget")),city:fd.get("city"),guests:Number(fd.get("guests")),event_type:fd.get("event_type"),venue:fd.get("venue"),preferences:fd.get("preferences")};endpoint="/generate-party";
 } else {payload=new FormData(form);endpoint="/generate-jewelry";}
 const options=planner==="jewelry"?{method:"POST",body:payload}:{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)};
 try{const r=await fetch(endpoint,options),d=await r.json();if(!r.ok)throw new Error(d.detail||"Request failed");location.href="/recommendations/"+d.id}
 catch(err){message.textContent=err.message}
});
