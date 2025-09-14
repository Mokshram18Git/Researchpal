class ResearchPal {
    constructor() {
        this.initializeEventListeners();
        this.checkStatus();
        setInterval(() => this.checkStatus(), 5000); // Check status every 5 seconds
    }

    initializeEventListeners() {
        // File upload handling
        const fileInput = document.getElementById('fileInput');
        const uploadBox = document.getElementById('uploadBox');
        
        fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
        
        // Drag and drop
        uploadBox.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadBox.style.borderColor = '#3498db';
            uploadBox.style.background = '#f8f9fa';
        });
        
        uploadBox.addEventListener('dragleave', () => {
            uploadBox.style.borderColor = '#bdc3c7';
            uploadBox.style.background = 'transparent';
        });
        
        uploadBox.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadBox.style.borderColor = '#bdc3c7';
            uploadBox.style.background = 'transparent';
            
            if (e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                this.handleFileUpload(e);
            }
        });

        // Chat functionality
        document.getElementById('sendButton').addEventListener('click', () => this.askQuestion());
        document.getElementById('questionInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.askQuestion();
            }
        });

        // Key points button
        document.getElementById('keypointsButton').addEventListener('click', () => this.getKeyPoints());
    }

    async checkStatus() {
        try {
            const response = await fetch('/status');
            const data = await response.json();
            
            const statusBadge = document.getElementById('statusBadge');
            const sendButton = document.getElementById('sendButton');
            const keypointsButton = document.getElementById('keypointsButton');
            
            if (data.db_ready) {
                statusBadge.textContent = 'Ready';
                statusBadge.className = 'status-badge ready';
                sendButton.disabled = false;
                keypointsButton.disabled = false;
            } else {
                statusBadge.textContent = 'Upload PDF First';
                statusBadge.className = 'status-badge';
                sendButton.disabled = true;
                keypointsButton.disabled = true;
            }
        } catch (error) {
            console.error('Status check failed:', error);
        }
    }

    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        const uploadStatus = document.getElementById('uploadStatus');
        uploadStatus.textContent = 'Uploading and processing PDF...';
        uploadStatus.className = '';

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                uploadStatus.textContent = '✅ PDF uploaded and processing started!';
                uploadStatus.className = 'upload-success';
                this.addMessage('ResearchPal', 'PDF is being processed. I\'ll be ready to answer questions shortly!', 'ai');
            } else {
                uploadStatus.textContent = `❌ Error: ${data.error}`;
                uploadStatus.className = 'upload-error';
            }
        } catch (error) {
            uploadStatus.textContent = '❌ Upload failed. Please try again.';
            uploadStatus.className = 'upload-error';
            console.error('Upload error:', error);
        }
    }

    async askQuestion() {
        const input = document.getElementById('questionInput');
        const question = input.value.trim();
        
        if (!question) return;

        this.addMessage('You', question, 'user');
        input.value = '';

        const sendButton = document.getElementById('sendButton');
        sendButton.disabled = true;

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question })
            });

            const data = await response.json();

            if (response.ok) {
                this.addMessage('ResearchPal', data.answer, 'ai');
            } else {
                this.addMessage('Error', data.error, 'error');
            }
        } catch (error) {
            this.addMessage('Error', 'Failed to get response. Please try again.', 'error');
            console.error('Ask error:', error);
        } finally {
            sendButton.disabled = false;
        }
    }

    async getKeyPoints() {
        const button = document.getElementById('keypointsButton');
        button.disabled = true;

        this.addMessage('You', 'Get key points from this research', 'user');

        try {
            const response = await fetch('/keypoints');
            const data = await response.json();

            if (response.ok) {
                this.addMessage('ResearchPal', data.key_points, 'ai');
            } else {
                this.addMessage('Error', data.error, 'error');
            }
        } catch (error) {
            this.addMessage('Error', 'Failed to get key points. Please try again.', 'error');
            console.error('Key points error:', error);
        } finally {
            button.disabled = false;
        }
    }

    addMessage(sender, content, type = 'ai') {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>${sender}:</strong> ${content}
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new ResearchPal();
});