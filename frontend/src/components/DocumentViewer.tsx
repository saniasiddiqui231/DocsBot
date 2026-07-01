import React, { useEffect, useState } from "react";
import {
  Box,
  Center,
  Spinner,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Text,
} from "@chakra-ui/react";
import API_BASE_URL from "../config";

interface Props {
    file: File | null;
    onClose: () => void;
}

export default function DocumentViewer({
    file,
    onClose,
}: Props) {
  const [csvData, setCsvData] = useState<string[][]>([]);
  const [textData, setTextData] = useState("");

  useEffect(() => {
    if (!file) return;

    const extension = file.name.split(".").pop()?.toLowerCase();

    if (extension === "csv" || extension === "txt") {
      const reader = new FileReader();

      reader.onload = (e) => {
        const result = e.target?.result as string;

        if (extension === "csv") {
          const rows = result
            .split("\n")
            .map((row) => row.split(","));

          setCsvData(rows);
        }

        if (extension === "txt") {
          setTextData(result);
        }
      };

      reader.readAsText(file);
    }
  }, [file]);

  if (!file) {
    return (
      <Center h="100%">
        <Text color="gray.500">
          Upload a document to preview it.
        </Text>
      </Center>
    );
  }

  const extension = file.name.split(".").pop()?.toLowerCase();

  if (extension === "pdf") {
    const previewUrl = API_BASE_URL
      ? `${API_BASE_URL}/uploads/${encodeURIComponent(file.name)}`
      : `/uploads/${encodeURIComponent(file.name)}`;

    return (
      <iframe
        title="PDF Viewer"
        src={previewUrl}
        width="100%"
        height="100%"
        style={{
          border: "none",
        }}
      />
    );
  }

  if (extension === "csv") {
    if (csvData.length === 0) {
      return (
        <Center h="100%">
          <Spinner />
        </Center>
      );
    }

    return (
      <Box
        h="100%"
        overflow="auto"
        p={4}
      >
        <Table size="sm">
          <Thead>
            <Tr>
              {csvData[0].map((header, index) => (
                <Th key={index}>{header}</Th>
              ))}
            </Tr>
          </Thead>

          <Tbody>
            {csvData.slice(1).map((row, i) => (
              <Tr key={i}>
                {row.map((cell, j) => (
                  <Td key={j}>{cell}</Td>
                ))}
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    );
  }

  if (extension === "txt") {
    return (
      <Box
        h="100%"
        overflow="auto"
        p={6}
        whiteSpace="pre-wrap"
      >
        {textData}
      </Box>
    );
  }

  return (
    <Center h="100%">
      <Text textAlign="center">
        Preview not available.
        <br />
        You can still chat with this document.
      </Text>
    </Center>
  );
}