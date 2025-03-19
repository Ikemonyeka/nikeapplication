import { Box, Typography, Button } from "@mui/material";
import { Link } from "react-router-dom";
import image1 from '../assets/images/main-img.png'

export default function MainFeature() {
    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: { xs: "column", md: "row" },
                alignItems: "center",
                justifyContent: "space-between",
                padding: "30px", // Reduced padding
                backgroundColor: "#f5f5f5",
                borderRadius: "8px",
                boxShadow: "0px 3px 8px rgba(0,0,0,0.1)",
                margin: "15px auto",
                maxWidth: "1000px", // Reduced width
                textAlign: { xs: "center", md: "left" },
            }}
        >
            {/* Left Side - Text Content */}
            <Box sx={{ flex: 1, paddingRight: { md: "15px" } }}>
                <Typography variant="h5" sx={{ fontWeight: "bold", color: "#333", marginBottom: "8px" }}>
                    Elevate Your Run with Nike
                </Typography>
                <Typography variant="body2" sx={{ color: "#555", marginBottom: "15px" }}>
                    Experience comfort and performance with our latest running shoes. Designed for speed, stability, and
                    durability.
                </Typography>
                <Button
                    component={Link}
                    to="/products"
                    variant="contained"
                    sx={{
                        backgroundColor: "#f04a00",
                        color: "white",
                        padding: "8px 16px", // Reduced button size
                        fontSize: "14px",
                        "&:hover": { backgroundColor: "#d93d00" },
                    }}
                >
                    Shop Now
                </Button>
            </Box>

            {/* Right Side - Shoe Image */}
            <Box
                sx={{
                    flex: 1,
                    display: "flex",
                    justifyContent: "center",
                }}
            >
                <img
                    src={image1}
                    style={{ width: "80%", maxWidth: "360px", height: "auto", borderRadius: "8px" }} // Reduced image size
                />
            </Box>
        </Box>
    );
}
