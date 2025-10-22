// Simple Node.js script to test our APIs
const http = require('http');

function testAPI(path, data) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(data);
    
    const options = {
      hostname: 'localhost',
      port: 3001,
      path: path,
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
        console.log(`✓ ${path} - Status: ${res.statusCode}`);
        console.log(`  Response: ${data}\n`);
        resolve({ status: res.statusCode, data });
      });
    });

    req.on('error', (e) => {
      console.log(`✗ ${path} - Error: ${e.message}\n`);
      reject(e);
    });

    req.write(postData);
    req.end();
  });
}

async function runTests() {
  console.log('Testing API endpoints...\n');

  // Test Contact API
  try {
    await testAPI('/api/contact', {
      name: 'Test User',
      email: 'test@example.com',
      subject: 'Test Subject',
      message: 'This is a test message from the API test script.'
    });
  } catch (e) {
    console.log('Contact API test failed');
  }

  // Test Appointments API
  try {
    await testAPI('/api/appointments', {
      firstName: 'John',
      lastName: 'Doe',
      email: 'john@example.com',
      phone: '+44 123 456 7890',
      consultationType: 'In-Person Consultation',
      location: 'London Studio',
      projectType: 'Engagement Ring',
      budgetRange: '£5,000 - £10,000',
      projectDescription: 'Looking for a custom diamond engagement ring',
      preferredDateTime: '2024-02-15T10:00'
    });
  } catch (e) {
    console.log('Appointments API test failed');
  }

  // Test Newsletter API
  try {
    await testAPI('/api/newsletter', {
      email: 'newsletter@example.com'
    });
  } catch (e) {
    console.log('Newsletter API test failed');
  }

  // Test Sizing API
  try {
    await testAPI('/api/sizing', {
      name: 'Test User',
      email: 'sizing@example.com',
      currentSize: '6',
      requestedSize: '7',
      ringType: 'Engagement Ring',
      notes: 'Need ring resized urgently'
    });
  } catch (e) {
    console.log('Sizing API test failed');
  }

  console.log('API testing completed!');
}

runTests();