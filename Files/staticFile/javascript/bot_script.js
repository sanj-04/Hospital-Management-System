const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");

let userMessage = null; // Variable to store user's message
const API_KEY = window.ApiKey;"PASTE-YOUR-API-KEY"; // Paste your API key here
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className, class_list="") => {
    // Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    if (class_list != "") {
        chatLi.querySelector("p").classList.add(class_list);
    }
    return chatLi; // return chat <li> element
}

const createChatBtn = (btn_text, className, btn_id) => {
    let chatBtn = document.createElement("button");
    chatBtn.setAttribute("type", "button");
    chatBtn.setAttribute("class", className);
    chatBtn.setAttribute("id", btn_id);
    chatBtn.innerText = btn_text;
    return chatBtn; // return chat <button> element
}

function handleOpt(){
    console.log(this);
    let outgoingChatLi = createChatLi(this.innerText, "outgoing");
    chatbox.appendChild(outgoingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    setTimeout(() => {
        // Display "Thinking..." message while waiting for the response
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi, option_id=this.id);
    }, 600);

    document.querySelectorAll(".chat_option").forEach(el=>{
        el.remove();
    });
    // var elm= document.createElement("p");
    // elm.setAttribute("class","test");
    // var sp= '<span class="rep">'+this.innerText+'</span>';
    // elm.innerHTML= sp;
    // cbot.appendChild(elm);

    // console.log(findText.toLowerCase());
    // var tempObj= data[findText.toLowerCase()];
    // handleResults(tempObj.title,tempObj.options,tempObj.url);
}

function handleOuterOpt(ele){
    btn_text = ele.getAttribute("data-text")
    let outgoingChatLi = createChatLi(btn_text, "outgoing");
    chatbox.appendChild(outgoingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    setTimeout(() => {
        // Display "Thinking..." message while waiting for the response
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi, option_id=ele.id);
    }, 600);

    document.querySelectorAll(".chat_option").forEach(el=>{
        el.remove();
    });
}

// const generateResponse = (chatElement) => {
//     const API_URL = window.ApiUrl; //"https://api.openai.com/v1/chat/completions";
//     const messageElement = chatElement.querySelector("p");

//     // Define the properties and message for the API request
//     const requestOptions = {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//             "Authorization": `Bearer ${API_KEY}`,
//         },
//         body: JSON.stringify({
//             csrfmiddlewaretoken: `${CSRF_TOKEN}`,
//             model: "gpt-3.5-turbo",
//             messages: [{role: "user", content: userMessage}],
//         })
//     }

//     // Send POST request to API, get response and set the reponse as paragraph text
//     fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
//         messageElement.textContent = data.choices[0].message.content.trim();
//     }).catch(() => {
//         messageElement.classList.add("error");
//         messageElement.textContent = "Oops! Something went wrong. Please try again.";
//     }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
// }

const generateResponse = (chatElement, option_id=null) => {
    const messageElement = chatElement.querySelector("p");
    $.ajax({
        url : window.ApiUrl,
        type : "POST",
        data : {
            'csrfmiddlewaretoken': window.CsrfToken,
            'role': "user",
            'content': userMessage,
            'option_id': option_id,
        },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", window.CsrfToken);
        },
        success : function(data,textMsg, xhr) {
            console.log(data.response, data.response.length);
            if (data.response.length > 1) {
                data.response.forEach((element, index) => {
                    if (index == 0) {
                        messageElement.textContent = element.text;
                        if (element.class_list != "") {
                            messageElement.classList.add(element.class_list);
                        }
                    } else {
                        let incomingChatLi = createChatLi(element.text, "incoming", element.class_list);
                        chatbox.appendChild(incomingChatLi);
                        chatbox.scrollTo(0, chatbox.scrollHeight);
                    }
                });
            } else {
                messageElement.textContent = data.response[0].text;
                if (data.response[0].class_list != "") {
                    messageElement.classList.add(data.response[0].class_list);
                }
            }

            console.log(data.options, data.options.length);
            if (data.options.length != 0) {
                data.options.forEach((element, index) => {
                    let incomingChatBtn = createChatBtn(
                        element.text,
                        element.class_list,
                        element.option_id
                    );
                    chatbox.appendChild(incomingChatBtn);
                    chatbox.scrollTo(0, chatbox.scrollHeight);
                    incomingChatBtn.addEventListener("click", handleOpt);
                });
            }
        },
        error : function(xhr, errmsg, err) {
            messageElement.classList.add("error");
            messageElement.textContent = "Oops! Something went wrong. Please try again.";
        },
        statusCode: {
            401: function() {
                window.scrollTo(0, 0);
                location.reload();
            }
        }
    });
    chatbox.scrollTo(0, chatbox.scrollHeight);
}

const handleChat = () => {
    userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
    if(!userMessage) return;

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the user's message to the chatbox
    console.log(userMessage);
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);
    
    setTimeout(() => {
        // Display "Thinking..." message while waiting for the response
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
}

chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window 
    // width is greater than 800px, handle the chat
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

sendChatBtn.addEventListener("click", handleChat);
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));