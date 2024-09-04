document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-full').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = function(event){
    event.preventDefault();

    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        load_mailbox('sent');
    });    

  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-full').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

      console.log(emails);

      emails.forEach(email =>{
      
        const mailDiv = document.createElement('div');
        mailDiv.classList.add('email-header');
        mailDiv.addEventListener('click', function() {
          mark_read(email.id)
          view_mail(email.id, mailbox)
          
      });

        if (email.read) {
          mailDiv.classList.add('email-read');
        } else {
          mailDiv.classList.add('email-unread');
        }

        mailDiv.innerHTML = `
            <span class="email-sender"><strong>${email.sender}</strong></span>
            <span class="email-subject">${email.subject}</span>
            <span class="email-timestamp">${email.timestamp}</span>
        `;

        document.querySelector('#emails-view').append(mailDiv);
        
      });
      
  });
}

function view_mail(id, mailbox_){

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-full').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    document.querySelector('#email-full').innerHTML = '';

    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        // Print email
        console.log(email);
    
        const mailDiv = document.createElement('div');

        if (email.archived === false && mailbox_ !== 'sent'){
          mailDiv.innerHTML = `
          <button id="archive">Archive</button>
      `;
        }
        else if (email.archived === true && mailbox_ !== 'sent'){
          mailDiv.innerHTML = `
          <button id="unarchive">Unarchive</button>
      `;
        }
        
          mailDiv.innerHTML += `
          <p ><strong>From: </strong>${email.sender}</p>
          <p ><strong>To: </strong>${email.recipients}</p>
          <p ><strong>Subject: </strong>${email.subject}</p>
          <p ><strong>Timestamp: </strong>${email.timestamp}</p>
           <p class="email-body">${email.body}</p>
           <button id="reply">Reply</button>
      `;          
       


        document.querySelector('#email-full').append(mailDiv);

        if (document.querySelector('#archive')){
          document.querySelector('#archive').onclick = function (){
            archive_mail(email.id)
            load_mailbox('inbox')
          }
        }

        if (document.querySelector('#unarchive')){
          document.querySelector('#unarchive').onclick = function (){
            unarchive_mail(email.id)
            load_mailbox('inbox')
          }
        }

        document.querySelector('#reply').onclick = function (){
          reply(email.sender, email.subject, email.timestamp, email.body)
        }


    });
}

function reply(email_sender, email_subject, email_timestamp, email_body){

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-full').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
  
    // Pre-fill 
    document.querySelector('#compose-recipients').value = `${email_sender}`;
    document.querySelector('#compose-subject').value = `Re: ${email_subject}`;
    document.querySelector('#compose-body').value = `\n\n On ${email_timestamp} ${email_sender} wrote: \n ${email_body}`;
  
    document.querySelector('#compose-form').onsubmit = function(event){
      event.preventDefault();
  
      const recipients = document.querySelector('#compose-recipients').value;
      const subject = document.querySelector('#compose-subject').value;
      const body = document.querySelector('#compose-body').value;
  
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
      })
      .then(response => response.json())
      .then(result => {
          console.log(result);
          load_mailbox('sent');
      });    
  
    }

}

function mark_read(id){

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

}

function archive_mail(id){

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })

}

function unarchive_mail(id){

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })

}
