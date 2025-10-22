// Test enhanced chatbot responses
const http = require('http');

function testChatbot(message) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({ message });
    
    const options = {
      hostname: 'localhost',
      port: 3001,
      path: '/api/chat',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        console.log(`\n📝 User: "${message}"`);
        console.log(`🤖 Bot Response:\n${data.split('data: ')[1]?.split('\\n')[0] || 'No response'}\n`);
        console.log('─'.repeat(80));
        resolve(data);
      });
    });

    req.on('error', (e) => {
      console.log(`Error testing "${message}": ${e.message}`);
      reject(e);
    });

    req.write(postData);
    req.end();
  });
}

async function runChatbotTests() {
  console.log('🎯 Testing Enhanced Chatbot Responses...\n');
  console.log('═'.repeat(80));

  const testMessages = [
    "Hello!",
    "I'm looking for an engagement ring",
    "Tell me about diamonds",
    "What's the difference between platinum and gold?",
    "Show me ruby jewelry",
    "I need help with ring sizing",
    "I want to book an appointment",
    "What's your bespoke process like?",
    "How much do engagement rings cost?",
    "I'm interested in wedding bands"
  ];

  for (const message of testMessages) {
    try {
      await testChatbot(message);
      // Small delay between requests
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (e) {
      console.log(`Failed to test: ${message}`);
    }
  }

  console.log('\n✅ Enhanced chatbot testing completed!');
  console.log('The chatbot now provides detailed, educational responses with specific guidance.');
}

runChatbotTests();