import React from "react";
import {
  Box,
  Button,
  Input,
  Text,
  VStack,
  Alert,
  AlertIcon,
  Spinner,
} from "@chakra-ui/react";

interface Props {
  file: File | null;
  uploadResult: string;
  loading: boolean;
  onFileChange: (
    event: React.ChangeEvent<HTMLInputElement>
  ) => void;
}

export default function UploadPanel({
  file,
  uploadResult,
  loading,
  onFileChange,
}: Props) {
  return (
    <Box
      bg="white"
      p={5}
      borderBottom="1px solid"
      borderColor="gray.200"
    >
      <VStack align="stretch" spacing={4}>
        <Text
          fontWeight="bold"
          fontSize="lg"
        >
          Upload Document
        </Text>

        <Input
          type="file"
          accept=".pdf,.doc,.docx,.txt,.csv"
          onChange={onFileChange}
          isDisabled={loading}
        />

        {file && (
          <Box
            p={3}
            bg="gray.50"
            borderRadius="md"
          >
            <Text
              fontWeight="semibold"
            >
              Selected File
            </Text>

            <Text
              color="gray.600"
              fontSize="sm"
            >
              {file.name}
            </Text>
          </Box>
        )}

        {loading && (
          <Box
            display="flex"
            alignItems="center"
            gap={3}
          >
            <Spinner />

            <Text>
              Preparing chatbot...
            </Text>
          </Box>
        )}

        {uploadResult && (
          <Alert
            status="success"
            borderRadius="md"
          >
            <AlertIcon />
            {uploadResult}
          </Alert>
        )}
      </VStack>
    </Box>
  );
}