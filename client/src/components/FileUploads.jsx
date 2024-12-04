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
      const base64Data = reader.result.split(",")[1]; // Extract base64 string
      try {
        setLoading(true);
        setError(null);

        const response = await axios.post(
          `${BASE_URL}/api/uploads/`,
          { file_data: base64Data },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
              "Content-Type": "application/json",
            },
          }
        );

        setAttachment(response.data.upload); // Save uploaded file metadata
        console.log("Upload successful:", response.data);
      } catch (err) {
        console.error("Error uploading file:", err.response?.data || err.message);
        setError("Failed to upload file");
      } finally {
        setLoading(false);
      }
    };

    reader.readAsDataURL(file); // Convert file to base64
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
