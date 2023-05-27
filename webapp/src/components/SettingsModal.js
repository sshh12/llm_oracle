import React from 'react';
import {
  Text,
  VStack,
  Input,
  Button,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  FormControl,
  FormLabel,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  Checkbox,
} from '@chakra-ui/react';
import { SettingsIcon } from '@chakra-ui/icons';

function SettingsModal({
  modelTemp,
  setModelTemp,
  publicVisable,
  setPublicVisable,
  setRecentResults,
  userId,
}) {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <>
      <Button
        m={2}
        onClick={onOpen}
        rightIcon={<SettingsIcon />}
        colorScheme="teal"
        variant="solid"
      >
        Settings
      </Button>

      <Modal onClose={onClose} isOpen={isOpen} isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Settings</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <VStack spacing={6}>
              <FormControl>
                <FormLabel>User ID</FormLabel>
                <Text pb={'4px'}>
                  Purchased credits are tied to your user ID.
                </Text>
                <Input value={userId} disabled={true} />
              </FormControl>
              <FormControl>
                <FormLabel>Model Temperature</FormLabel>
                <Slider
                  defaultValue={modelTemp}
                  onChange={v => setModelTemp(v)}
                >
                  <SliderTrack>
                    <SliderFilledTrack />
                  </SliderTrack>
                  <SliderThumb />
                </Slider>
              </FormControl>
              <FormControl>
                <FormLabel>Public Predictions</FormLabel>
                <Checkbox
                  isChecked={publicVisable}
                  onChange={e => setPublicVisable(e.target.checked)}
                >
                  Viewable By Public
                </Checkbox>
              </FormControl>
              <FormControl>
                <FormLabel>Prediction History</FormLabel>
                <Text pb={'4px'}>
                  This does not delete predictions from the server, UI only.
                </Text>
                <Button colorScheme="red" onClick={() => setRecentResults([])}>
                  Clear History
                </Button>
              </FormControl>
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button onClick={onClose}>Close & Save</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}

export default SettingsModal;
