import { Box, Center, Spinner, Text } from "@chakra-ui/react";
import { useEffect, useRef } from "react";

import MessageBubble from "./MessageBubble";
import { Message } from "../types/chat";

interface Props {
  messages: Message[];
  loading: boolean;
  error: string;
  hasFile: boolean;
  uploadResult: string;
}
export default function ChatWindow({
  messages,
  loading,
  error,
  hasFile,
  uploadResult,
}: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <Box
      flex="1"
      overflowY="auto"
      p={5}
      bg="gray.50"
    >
      {/* Empty State */}
      {!hasFile && messages.length === 0 && !loading && (
        <Center
          h="100%"
          flexDirection="column"
        >
          <Text fontSize="5xl">📄</Text>

          <Text
            mt={4}
            fontWeight="bold"
            fontSize="lg"
          >
            Upload a document to start chatting
          </Text>

          <Text
            mt={2}
            color="gray.500"
            textAlign="center"
          >
            Ask questions about your resume,
            PDF, report or notes.
          </Text>
        </Center>
      )}
      {hasFile && messages.length === 0 && !loading && (
  <Center h="100%" flexDirection="column">
    <Text fontSize="5xl">✅</Text>

    <Text mt={4} fontWeight="bold">
      Document uploaded successfully!
    </Text>

    <Text color="gray.500" mt={2}>
      {uploadResult || "You can now ask questions about your document."}
    </Text>
  </Center>
)}

      {/* Chat Messages */}
      {messages.map((message, index) => (
        <MessageBubble
          key={index}
          message={message}
        />
      ))}

      {/* Loading */}
      {loading && (
        <Box
          display="flex"
          alignItems="center"
          gap={3}
          mt={3}
        >
          <Spinner size="sm" />

          <Text color="gray.600">
            Gemini is thinking...
          </Text>
        </Box>
      )}

      {/* Error */}
      {error && (
        <Box
          mt={4}
          p={3}
          borderRadius="md"
          bg="red.50"
        >
          <Text color="red.600">
            {error}
          </Text>
        </Box>
      )}

      <div ref={bottomRef} />
    </Box>
  );
}