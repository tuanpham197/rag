<script setup>
import { ref, nextTick, onMounted } from 'vue';

const messages = ref([
  { id: 1, text: "Hello! How can I help you today?", sender: 'other', timestamp: new Date(Date.now() - 60000) },
  { id: 2, text: "I'm looking for a premium chat UI.", sender: 'me', timestamp: new Date(Date.now() - 30000) },
]);

const newMessage = ref("");
const messagesContainer = ref(null);

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const sendMessage = () => {
  if (!newMessage.value.trim()) return;
  
  messages.value.push({
    id: Date.now(),
    text: newMessage.value,
    sender: 'me',
    timestamp: new Date()
  });
  
  newMessage.value = "";
  scrollToBottom();

  // Simulate response
  setTimeout(() => {
    messages.value.push({
      id: Date.now() + 1,
      text: "That sounds great! This UI is built with Vue.js and features a modern glassmorphism design.",
      sender: 'other',
      timestamp: new Date()
    });
    scrollToBottom();
  }, 1000);
};

onMounted(() => {
  scrollToBottom();
});
</script>

<template>
  <div class="chat-container">
    <div class="chat-header">
      <div class="avatar">
        <i class="fas fa-robot"></i>
      </div>
      <div class="header-info">
        <h3>AI Assistant</h3>
        <span class="status">Online</span>
      </div>
      <button class="icon-btn"><i class="fas fa-ellipsis-v"></i></button>
    </div>

    <div class="messages-area" ref="messagesContainer">
      <div v-for="msg in messages" :key="msg.id" :class="['message-wrapper', msg.sender]">
        <div class="message-bubble">
          {{ msg.text }}
          <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
        </div>
      </div>
    </div>

    <div class="input-area">
      <button class="icon-btn record-btn">
        <i class="fas fa-microphone"></i>
      </button>
      <input 
        v-model="newMessage" 
        @keyup.enter="sendMessage"
        type="text" 
        placeholder="Type a message..." 
      />
      <button class="send-btn" @click="sendMessage">
        <i class="fas fa-paper-plane"></i>
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  width: 100%;
  max-width: 450px;
  height: 600px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.chat-header {
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.avatar {
  width: 45px;
  height: 45px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.header-info h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.status {
  font-size: 0.8rem;
  opacity: 0.9;
  display: flex;
  align-items: center;
  gap: 5px;
}

.status::before {
  content: '';
  width: 8px;
  height: 8px;
  background: #4ade80;
  border-radius: 50%;
  display: block;
}

.messages-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: #f8f9fa;
}

.message-wrapper {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.message-wrapper.me {
  align-self: flex-end;
  align-items: flex-end;
}

.message-wrapper.other {
  align-self: flex-start;
  align-items: flex-start;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
  font-size: 0.95rem;
  line-height: 1.4;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  animation: fadeIn 0.3s ease;
}

.me .message-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.other .message-bubble {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
}

.timestamp {
  display: block;
  font-size: 0.7rem;
  margin-top: 5px;
  opacity: 0.7;
  text-align: right;
}

.input-area {
  padding: 15px;
  background: white;
  display: flex;
  align-items: center;
  gap: 10px;
  border-top: 1px solid #eee;
}

input {
  flex: 1;
  padding: 12px 15px;
  border: 2px solid #eee;
  border-radius: 25px;
  outline: none;
  transition: all 0.3s;
  font-family: inherit;
}

input:focus {
  border-color: #764ba2;
  background: #fdfdfd;
}

.icon-btn {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  font-size: 1.1rem;
  transition: color 0.3s;
  padding: 8px;
}

.icon-btn:hover {
  color: #764ba2;
}

.send-btn {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 10px rgba(118, 75, 162, 0.3);
}

.send-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 15px rgba(118, 75, 162, 0.4);
}

.send-btn:active {
  transform: scale(0.95);
}

/* Scrollbar Styling */
.messages-area::-webkit-scrollbar {
  width: 6px;
}

.messages-area::-webkit-scrollbar-track {
  background: transparent;
}

.messages-area::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 3px;
}

.messages-area::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
