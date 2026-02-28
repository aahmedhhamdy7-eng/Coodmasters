document.addEventListener('DOMContentLoaded',()=>{

  // ABOUT PAGE Q&A
  const sendBtn=document.getElementById('sendBtn');
  if(sendBtn){
    sendBtn.addEventListener('click',()=>{
      const questionInput=document.getElementById('userQuestion');
      const responseDiv=document.getElementById('response');
      const question=questionInput.value.trim();
      if(question===''){ alert('Veuillez écrire une question avant d’envoyer.'); return; }
      responseDiv.innerText="Merci, j’ai bien reçu votre question. Je vous répondrai dans 3 jours environ.";
      responseDiv.classList.add('showResponse');
      questionInput.value='';
    });
  }

  // CONTACT PAGE
  const contactButtons=document.querySelectorAll('.contact-btn');
  const infoDisplay=document.getElementById('infoDisplay');
  if(contactButtons && infoDisplay){
    contactButtons.forEach(btn=>{
      btn.addEventListener('click',()=>{
        const type=btn.dataset.type;
        let html='';
        if(type==='prof') html=`<p>Math: math@unihelp.com</p><p>Physique: phys@unihelp.com</p><p>Info: info@unihelp.com</p>`;
        if(type==='assist') html=`<p>Assistant 1: assist1@unihelp.com</p><p>Assistant 2: assist2@unihelp.com</p><p>Assistant 3: assist3@unihelp.com</p>`;
        if(type==='stage') html=`<p>Stage 1: stage1@unihelp.com</p><p>Stage 2: stage2@unihelp.com</p><p>Stage 3: stage3@unihelp.com</p>`;
        infoDisplay.innerHTML=html;
      });
    });
  }
  function sendQuestion() {
    let question = document.getElementById("question").value;
    fetch("/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question: question})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText = data.response;
    });
}
function sendQuestion() {
    let question = document.getElementById("question").value;

    // Envoie la question à Flask
    fetch("/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question: question})
    })
    .then(res => res.json())
    .then(data => {
        // Affiche la réponse dans la page
        document.getElementById("result").innerText = data.response;
    });
}
});