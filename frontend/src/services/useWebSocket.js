import { useEffect, useRef, useState, useCallback } from 'react';
import { generate } from "random-words";

export const useWebSocket = (url) => {
    const [response, setResponse] = useState(''); // Stores bot responses
    const [isOpen, setIsOpen] = useState(false); // WebSocket connection status
    const [isBotResponseComplete, setIsBotResponseComplete] = useState(false); // Tracks completion of bot response
    const socketRef = useRef(null); // WebSocket reference
    const wordUUIDRef = useRef(generate({ exactly: 4 }).join('-')); // Conversation UUID
    const messageQueueRef = useRef([]); // Queue for unsent messages
    const retryCountRef = useRef(0); // Tracks reconnection attempts
    const maxRetries = 5; // Max number of reconnection attempts

    const connectSocket = useCallback(() => {
        const socket = new WebSocket(url);
        socketRef.current = socket;

        socket.onopen = () => {
            console.log('WebSocket connection opened for', wordUUIDRef.current);
            setIsOpen(true);
            retryCountRef.current = 0;
            socket.send(JSON.stringify({ uuid: wordUUIDRef.current, init: true })); // Send initial connection message

            // Send queued messages once connection is open
            while (messageQueueRef.current.length > 0) {
                const message = messageQueueRef.current.shift();
                if (message) {
                    sendMessage(message);
                }
            }
        };

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                console.log('Received from server:', data);

                if (data.on_chat_model_stream) {
                    setResponse((prevResponse) => prevResponse + data.on_chat_model_stream); // Streamed response handling
                }

                if (data.on_chat_model_end) {
                    setIsBotResponseComplete(true); // Bot streaming is done, message complete
                }
            } catch (error) {
                console.log('Error parsing WebSocket message:', error);
            }
        };

        socket.onclose = () => {
            console.log('WebSocket connection closed');
            setIsOpen(false);

            if (retryCountRef.current < maxRetries) {
                retryCountRef.current += 1;
                console.log(`Attempting to reconnect (${retryCountRef.current}/${maxRetries}) in 3 seconds...`);
                setTimeout(connectSocket, 3000); // Retry connection after a 3 sec delay
            } else {
                console.log('Max reconnection attempts reached. Stopping reconnection.');
            }
        };

        socket.onerror = (error) => {
            console.log('WebSocket error:', error);
        };
    }, [url]);

    useEffect(() => {
        connectSocket();

        return () => {
            if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
                socketRef.current.close(); // Close connection on cleanup
            }
        };
    }, [connectSocket]);

    const sendMessage = (message) => {
        if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            const payload = {
                uuid: wordUUIDRef.current,
                message,
                init: false
            };
            socketRef.current.send(JSON.stringify(payload)); // Send message to WebSocket server
            setIsBotResponseComplete(false);
            setResponse(''); // Clear previous response before new message is processed
        } else {
            console.log('WebSocket connection is not open, queuing message:', message);
            messageQueueRef.current.push(message); // Queue message if connection is closed
        }
    };

    return { response, isOpen, isBotResponseComplete, sendMessage };
};