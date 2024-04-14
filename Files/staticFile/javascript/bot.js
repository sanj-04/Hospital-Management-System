// Define an array to store the conversation history
let conversationHistory = [];

// Flag to track if the bot is asking for patient ID
let isAskingForPatientID = false;

// Function to handle user input
function handleUserInput(userInput,bot=false) {
  // Add the user's input to the conversation history
  if (userInput && !bot) {
    conversationHistory.push(User: ${userInput});
  } else if (userInput && bot) {
    conversationHistory.push(Bot: ${userInput});
  }

  
  // Define the bot's response based on the user's input
  let botResponse;
  if (userInput && userInput.includes('hello')) {
    botResponse = 'Hello there! How can I assist you today?';
  } else if (userInput && userInput.includes('bye')) {
    botResponse = 'Goodbye! Have a great day.';
  } else if (!userInput) {
    botResponse = 'Hello, how can I help you?';
    showAppointmentButtons();
  } else if (isAskingForPatientID) {
    // Check if the user input is a number (patient ID)
    if (!isNaN(userInput)) {
      // Send an AJAX request to verify the patient ID
      verifyPatientID(userInput);
      botResponse = ''; // Do not display any response yet
    } else {
      botResponse = ''; // Do not display any response for invalid input
    }
  } else {
    botResponse = "I'm sorry, I didn't understand your request. The bot currently accepts to book appointments only";
  }

  // Add the bot's response to the conversation history (if there is a response)
  if (botResponse) {
    conversationHistory.push(Bot: ${botResponse});
  }

  // Display the conversation history in the chat interface
  displayConversation();
}

function verifyPatientID(patientId) {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'verifypatientid4.php', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      const response = xhr.responseText;
      if (response === 'Congratulations') {
        conversationHistory.push(Bot: ${response});
        generateTokenNumber(patientId);
      } else {
        conversationHistory.push(Bot: ${response});
        isAskingForPatientID = true;
        handleUserInput('Please provide a valid patient ID (a number).');
        displayConversation();
      }
    }
  };
  xhr.send('patientId=' + encodeURIComponent(patientId));
}

function generateTokenNumber(patientId) {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'generate_token.php', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      const tokenOutput = xhr.responseText.trim();
      if (tokenOutput) {
        conversationHistory.push(Bot: ${tokenOutput});
        hideAllButtons();
        showBackButton();
        displayConversation();
      } else {
        conversationHistory.push(Bot: Sorry, an error occurred while generating the token number.);
        displayConversation();
      }
    }
  };
  xhr.send('patientId=' + encodeURIComponent(patientId));
}

// Function to display the conversation history in the chat interface
function displayConversation() {
  const chatLog = document.getElementById('chat-log');
  chatLog.innerHTML = '';

  for (const message of conversationHistory) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('d-flex', 'mb-2');

    const senderElement = document.createElement('div');
    senderElement.classList.add('fw-bold', 'me-2');
    senderElement.textContent = message.split(': ')[0] + ':';

    const messageTextElement = document.createElement('div');
    messageTextElement.textContent = message.split(': ')[1];

    messageElement.appendChild(senderElement);
    messageElement.appendChild(messageTextElement);
    chatLog.appendChild(messageElement);
  }

  // Scroll to the bottom of the chat log
  chatLog.scrollTop = chatLog.scrollHeight;
}

// Function to show the appointment buttons
function showAppointmentButtons() {
  const appointmentButtonsContainer = document.getElementById('appointment-buttons-container');
  appointmentButtonsContainer.classList.remove('d-none');
}

// Function to hide all buttons
function hideAllButtons() {
  const appointmentButtonsContainer = document.getElementById('appointment-buttons-container');
  appointmentButtonsContainer.classList.add('d-none');
  const backButtonContainer = document.getElementById('back-button-container');
  backButtonContainer.classList.add('d-none');
}

// Function to show the back button
function showBackButton() {
  const backButtonContainer = document.getElementById('back-button-container');
  backButtonContainer.classList.remove('d-none');
}

// Function to hide the back button
function hideBackButton() {
  const backButtonContainer = document.getElementById('back-button-container');
  backButtonContainer.classList.add('d-none');
}

// Toggle the chat container visibility
function toggleChatContainer() {
  const chatContainer = document.getElementById('chat-container');
  chatContainer.classList.toggle('hidden');

  // Clear the conversation history and display the initial greeting message when the chat container is shown
  if (!chatContainer.classList.contains('hidden')) {
    conversationHistory = [];
    isAskingForPatientID = false;
    hideBackButton();
    handleUserInput('');
  }
}

// Initialization function
function init() {
  handleUserInput('');
}

// Call the initialization function when the page loads
window.addEventListener('load', init);

// Event listener for the open chat button
const openChatButton = document.getElementById('open-chat');
openChatButton.addEventListener('click', toggleChatContainer);

// Event listener for the close chat button
const closeChatButton = document.getElementById('close-chat');
closeChatButton.addEventListener('click', toggleChatContainer);

// Event listener for the book appointment button
const bookAppointmentButton = document.getElementById('book-appointment');
bookAppointmentButton.addEventListener('click', () => {
  hideAllButtons();
  isAskingForPatientID = true;
  handleUserInput('Please provide patient ID',true);
});

const backButton = document.getElementById('back-button');
backButton.addEventListener('click', () => {
  conversationHistory = [];
  isAskingForPatientID = false;
  hideBackButton();
  //handleUserInput('');
});

// Event listener for user input submission
const userInputForm = document.getElementById('user-input-form');
userInputForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const userInput = document.getElementById('user-input').value;
  handleUserInput(userInput);
  document.getElementById('user-input').value = '';
});