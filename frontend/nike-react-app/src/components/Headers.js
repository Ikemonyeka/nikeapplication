import { AppBar, Toolbar, Typography, IconButton, Drawer, List, ListItem, ListItemText, Box, Button, Modal, Paper } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import ChatIcon from "@mui/icons-material/Chat";
import CloseIcon from "@mui/icons-material/Close";
import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";

export default function Headers() {
    const [mobileOpen, setMobileOpen] = useState(false);
    const [chatOpen, setChatOpen] = useState(true);
    const [messages, setMessages] = useState([{ sender: "ai", text: "👋 Hi! How can I assist you today?" }]);
    const [inputText, setInputText] = useState("");
    const chatEndRef = useRef(null);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const toggleDrawer = () => setMobileOpen(!mobileOpen);
    const toggleChat = () => setChatOpen(!chatOpen);

    const handleSendMessage = async () => {
        if (inputText.trim() === "") return;
    
        const userMessage = { sender: "user", text: inputText };
        setMessages((prev) => [...prev, userMessage]);
        const API_BASE_URL = "http://127.0.0.1:8000";
    
        try {
            const response = await fetch(`${API_BASE_URL}/ai-agent/?user_message=${encodeURIComponent(inputText)}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({}) // Empty body since we pass the message in the query string
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log("API Response:", data); // Log the entire response for debugging
    
            // Handle the response when it's a string (simple response)
            if (typeof data === "string") {
                setMessages((prev) => [...prev, { sender: "ai", text: data }]);
            } 
            // Handle the response with recommendations
            else if (data.recommendations) {
                const recommendationText = data.recommendations
                    .map(item => `${item.name} - ${item.category} - $${item.price}`)
                    .join("<br />"); // Use HTML <br /> to break the line
    
                setMessages((prev) => [...prev, { sender: "ai", text: recommendationText }]);
            } 
            // Handle the order status response
            else if (data.order_images && data.order_number && data.status) {
                const orderImage = data.order_images;
                const orderStatus = data.status;
                const orderNumber = data.order_number;
    
                const orderMessage = `
                    <strong>Order #${orderNumber}</strong><br />
                    <img src="${orderImage}" alt="Order Image" style="max-width: 100%; height: auto; margin-top: 10px;" /><br />
                    <strong>Status:</strong> ${orderStatus}
                `;
                setMessages((prev) => [...prev, { sender: "ai", text: orderMessage }]);
            } 
            // Handle the case where there's no expected response format
            else {
                setMessages((prev) => [...prev, { sender: "ai", text: "Unexpected response from server" }]);
            }
        } catch (error) {
            console.error("Error fetching AI response:", error);
            setMessages((prev) => [...prev, { sender: "ai", text: "Error fetching response. Try again." }]);
        }
    
        setInputText("");
    };
    
    

    return (
        <>
            <AppBar position="static" sx={{ backgroundColor: "#333" }}>
                <Toolbar>
                    <IconButton edge="start" color="inherit" aria-label="menu" sx={{ display: { md: "none" } }} onClick={toggleDrawer}>
                        <MenuIcon />
                    </IconButton>

                    <Typography variant="h6" sx={{ flexGrow: 1, textDecoration: "none", color: "white", fontWeight: "bold" }}>
                        Nike AI Agent
                    </Typography>

                    <Box sx={{ display: { xs: "none", md: "flex" }, gap: "20px" }}>
                        {["Home", "Products", "About", "Contact"].map((text, index) => (
                            <Typography key={index} component={Link} to={`/${text.toLowerCase()}`} sx={{ color: "white", textDecoration: "none", fontSize: "16px", "&:hover": { color: "#f4a261" } }}>
                                {text}
                            </Typography>
                        ))}
                    </Box>
                </Toolbar>
            </AppBar>

            <Drawer anchor="left" open={mobileOpen} onClose={toggleDrawer}>
                <List sx={{ width: 250 }}>
                    {["Home", "Products", "About", "Contact"].map((text, index) => (
                        <ListItem button key={index} component={Link} to={`/${text.toLowerCase()}`} onClick={toggleDrawer}>
                            <ListItemText primary={text} />
                        </ListItem>
                    ))}
                </List>
            </Drawer>

            <Modal open={chatOpen} onClose={toggleChat} aria-labelledby="chat-modal" aria-describedby="chat-description">
                <Box sx={{ position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)", width: "60%", maxWidth: "600px", bgcolor: "background.paper", boxShadow: 24, borderRadius: "12px", p: 3 }}>
                    <Paper sx={{ p: 2, display: "flex", flexDirection: "column", height: "450px" }}>
                        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid #ddd", pb: 1 }}>
                            <Typography variant="h6" sx={{ fontWeight: "bold" }}>AI Assistant</Typography>
                            <IconButton onClick={toggleChat}>
                                <CloseIcon />
                            </IconButton>
                        </Box>

                        <Box sx={{ flex: 1, p: 2, overflowY: "auto", display: "flex", flexDirection: "column", gap: 1, maxWidth: "100%", wordWrap: "break-word" }}>
                            {messages.map((msg, index) => (
                                <Box key={index} sx={{ alignSelf: msg.sender === "user" ? "flex-end" : "flex-start", bgcolor: msg.sender === "user" ? "#f04a00" : "#e0e0e0", color: msg.sender === "user" ? "white" : "black", borderRadius: "8px", p: 1.5, maxWidth: "75%" }}>
                                    {/* If it's AI message, render HTML content for recommendations, otherwise plain text */}
                                    {msg.sender === "ai" && msg.text.includes("<br />") ? (
                                        <span dangerouslySetInnerHTML={{ __html: msg.text }} />
                                    ) : (
                                        msg.text
                                    )}
                                </Box>
                            ))}
                            <div ref={chatEndRef} />
                        </Box>

                        <Box sx={{ display: "flex", borderTop: "1px solid #ddd", pt: 1 }}>
                            <input type="text" value={inputText} onChange={(e) => setInputText(e.target.value)} placeholder="Type your message..." style={{ flex: 1, padding: "8px", borderRadius: "4px", border: "1px solid #ddd", outline: "none" }} onKeyDown={(e) => e.key === "Enter" && handleSendMessage()} />
                            <Button onClick={handleSendMessage} sx={{ ml: 1, bgcolor: "#f04a00", color: "white", "&:hover": { bgcolor: "#d93d00" } }}>
                                Send
                            </Button>
                        </Box>
                    </Paper>
                </Box>
            </Modal>

            <Button onClick={toggleChat} sx={{ position: "fixed", bottom: "20px", right: "20px", backgroundColor: "#f04a00", color: "white", borderRadius: "50%", width: "50px", height: "50px", minWidth: "unset", boxShadow: "0px 4px 6px rgba(0,0,0,0.2)", "&:hover": { backgroundColor: "#d93d00" } }}>
                <ChatIcon />
            </Button>
        </>
    );
}
