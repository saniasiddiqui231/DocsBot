import {
  Box,
  Button,
  Text,
} from "@chakra-ui/react";

interface Props {
  onNewChat: () => void;
}

export default function Header({
  onNewChat,
}: Props) {
  return (
    <Box
      h="60px"
      px={6}
      bg="white"
      borderBottom="1px solid"
      borderColor="gray.200"
      display="flex"
      alignItems="center"
      justifyContent="space-between"
      boxShadow="sm"
    >
      <Text
        fontSize="xl"
        fontWeight="bold"
      >
        📄 DocsBot
      </Text>

      <Button
        colorScheme="blue"
        onClick={onNewChat}
      >
        + New Chat
      </Button>
    </Box>
  );
}