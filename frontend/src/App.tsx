import React, { useState } from "react";
import {
  ChakraProvider,
  Box,
  Input,
} from "@chakra-ui/react";

import API_BASE_URL from "./config";

import Header from "./components/Header";
import DocumentViewer from "./components/DocumentViewer";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";

import { Message } from "./types/chat";

export default function App() {
  const [file, setFile] = useState<File | null>(null);

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState<Message[]>([]);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [uploadResult, setUploadResult] = useState("");

  const [, setSessionId] = useState("");

  const handleQuestionChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setQuestion(e.target.value);
  };
  const clearDocument = () => {
  setFile(null);
  setMessages([]);
  setQuestion("");
  setUploadResult("");
  setError("");
  setSessionId("");
};
  const newChat = () => {
  clearDocument();
};

  const handleFileChange = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) return;

    clearDocument();

    setFile(selectedFile);

    const formData = new FormData();

    formData.append("file", selectedFile);

    try {
      setLoading(true);

      const uploadResponse = await fetch(
        `${API_BASE_URL}/upload_process_file`,
        {
          method: "POST",
          body: formData,
        }
      );

      const uploadData = await uploadResponse.json();

      setUploadResult(uploadData.status);

      const prepareResponse = await fetch(
        `${API_BASE_URL}/prepare_chatbot?uploaded_filepath=${selectedFile.name}`,
        {
          method: "POST",
        }
      );

      const prepareData = await prepareResponse.json();

      setSessionId(prepareData.session_id);
    } catch (err) {
      console.error(err);

      setError("Unable to upload document.");
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!question.trim()) return;

    const userMessage = question;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: userMessage,
      },
    ]);

    setQuestion("");

    setLoading(true);

    setError("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/chat?query=${encodeURIComponent(
          userMessage
        )}`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unknown error."
        );
      }

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: data.result,
        },
      ]);
    } catch (err: any) {
      console.error(err);

      setError(
        err.message || "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <ChakraProvider>
      <Box
        h="100vh"
        display="flex"
        flexDirection="column"
        bg="gray.100"
      >
        <Header
    onNewChat={newChat}
/>

        <Box
  flex="1"
  display="flex"
  flexDirection={{
    base: "column-reverse",
    lg: "row",
  }}
  overflow="hidden"
>
          {/* PDF */}

          <Box
  w={{
    base: "100%",
    lg: "45%",
  }}
  h={{
    base: "40vh",
    lg: "100%",
  }}
  bg="white"
  borderRight="1px solid"
  borderColor="gray.200"
  overflow="hidden"
>
            <DocumentViewer
    file={file}
    onClose={clearDocument}
/>
          </Box>

          {/* CHAT */}

          <Box
  flex="1"
  display="flex"
  flexDirection="column"
  overflow="hidden"
  bg="gray.50"
>
            {!file && (
              <Box
                bg="white"
                p={5}
              >
                <Input
                  type="file"
                  accept=".pdf,.doc,.docx,.txt,.csv"
                  onChange={handleFileChange}
                />
              </Box>
            )}

            <ChatWindow
    messages={messages}
    loading={loading}
    error={error}
    hasFile={!!file}
    uploadResult={uploadResult}
/>

            {file && (
              <ChatInput
                question={question}
                loading={loading}
                onQuestionChange={
                  handleQuestionChange
                }
                onSend={sendMessage}
              />
            )}
          </Box>
        </Box>
      </Box>
    </ChakraProvider>
  );
}
