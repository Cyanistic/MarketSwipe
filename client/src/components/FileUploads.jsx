import { useRef, useState } from "react";
import axios from "axios";
import { BASE_URL } from '../App';

export default function useFileAttachment() {
  const fileInputRef = useRef(null);
  const [attachment, setAttachment] = useState(null); // Uploaded file metadata
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUploadClick = () => {
    if (!fileInputRef.current) {
      throw new Error("Input ref is null, idk how this happened");
    }
    fileInputRef.current.click();
  };

  const resetFile = () => {
    if (!fileInputRef.current) {
      throw new Error("Input ref is null, idk how this happened");
    }
    fileInputRef.current.value = "";
    setAttachment(null);
  };

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
  
    const reader = new FileReader();

    reader.onloadend = async () => {
      const base64Data = reader.result; // Entire Base64 string with MIME type
      console.log("Base64 Data Sent:", base64Data);
  
      try {
        const token = localStorage.getItem("token");
        const response = await axios.post(
          `${BASE_URL}/api/upload/`,
          {
            name: file.name,
            fileData: base64Data, // full Base64 string
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
  
        console.log("Upload successful:", response.data);
        setAttachment(response.data.upload); // Save uploaded file metadata
      } catch (error) {
        console.error("Error uploading file:", error.response?.data || error.message);
      }
    };
  
    reader.readAsDataURL(file); // Read file as Base64 with MIME type
  };
  

  const hiddenFileInput = () => (
    <input
      type="file"
      ref={fileInputRef}
      onChange={handleFileChange}
      style={{ display: "none" }}
    />
  );

  return {
    attachment,
    loading,
    error,
    hiddenFileInput,
    resetFile,
    handleFileUploadClick,
  };
}
