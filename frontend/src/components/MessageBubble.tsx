import { Box } from "@chakra-ui/react";
import { Message } from "../types/chat";

interface Props {
  message: Message;
}

export default function MessageBubble({
  message,
}: Props) {
  const isUser = message.sender === "user";

  return (
    <Box
      display="flex"
      justifyContent={
        isUser ? "flex-end" : "flex-start"
      }
      mb={4}
    >
      <Box
        maxW="75%"
        px={5}
        py={3}
        borderRadius="16px"
        bg={isUser ? "blue.500" : "white"}
        color={isUser ? "white" : "black"}
        boxShadow="sm"
      >
        {message.text}
      </Box>
    </Box>
  );
}