import React from "react";
import {
  Box,
  Button,
  HStack,
  Input,
} from "@chakra-ui/react";

interface Props {
  question: string;
  loading: boolean;
  onQuestionChange: (
    event: React.ChangeEvent<HTMLInputElement>
  ) => void;
  onSend: () => void;
}

export default function ChatInput({
  question = "",
  loading,
  onQuestionChange,
  onSend,
}: Props) {
  return (
    <Box
      bg="white"
      borderTop="1px solid"
      borderColor="gray.200"
      p={4}
    >
      <HStack spacing={3}>
        <Input
          placeholder="Ask anything about the document..."
          value={question}
          onChange={onQuestionChange}
          isDisabled={loading}
          onKeyDown={(e) => {
            if (
              e.key === "Enter" &&
              !loading &&
              question?.trim()
            ) {
              e.preventDefault();
              onSend();
            }
          }}
        />

        <Button
          colorScheme="blue"
          minW="90px"
          onClick={onSend}
          isLoading={loading}
          loadingText="Thinking..."
          isDisabled={loading || !question?.trim()}
        >
          Send
        </Button>
      </HStack>
    </Box>
  );
}