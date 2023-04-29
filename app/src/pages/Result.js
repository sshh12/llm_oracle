import React, { useState, useEffect, useCallback } from 'react';
import {
  Text,
  Link,
  VStack,
  Stack,
  Slider,
  Button,
  SliderMark,
  SliderTrack,
  Spinner,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
} from '@chakra-ui/react';
import {
  FacebookShareButton,
  FacebookIcon,
  RedditShareButton,
  RedditIcon,
  LinkedinShareButton,
  LinkedinIcon,
  TwitterShareButton,
  TwitterIcon,
} from 'react-share';
import { Alert, AlertIcon, AlertDescription } from '@chakra-ui/react';
import { SliderThumb } from '@chakra-ui/react';
import { ExternalLinkIcon, PlusSquareIcon, ChatIcon } from '@chakra-ui/icons';
import { get } from '../api';
import { useLocalStorage } from '../hooks';

function probabilityFormat(p) {
  if (p < 0.1) {
    return ['Very Unlikely', 'red.900'];
  } else if (p < 0.3) {
    return ['Unlikely', 'red.600'];
  } else if (p < 0.45) {
    return ['Somewhat Unlikely', 'orange.500'];
  } else if (p < 0.55) {
    return ['Even Odds', 'yellow.500'];
  } else if (p < 0.7) {
    return ['Somewhat Likely', 'green.600'];
  } else if (p < 0.9) {
    return ['Likely', 'green.800'];
  } else {
    return ['Very Likely', 'green.900'];
  }
}

function Result() {
  const jobId = window.location.pathname.split('/').at(-1);
  const [jobState, setJobState] = useState(null);
  useEffect(() => {
    const pollInterval = setInterval(() => {
      get(`jobs/${jobId}`).then(resp => {
        if (resp.state === 'error' || resp.state === 'complete') {
          clearInterval(pollInterval);
        }
        setJobState(resp);
      });
    }, 2000);
    get(`jobs/${jobId}`).then(resp => setJobState(resp));
    return () => {
      clearInterval(pollInterval);
    };
  }, [jobId]);

  const [recentResults, setResultResults] = useLocalStorage(
    'oracle:recent',
    () => []
  );
  const addRecent = useCallback(
    job => {
      setResultResults([
        ...recentResults.filter(item => item.id !== job.id),
        {
          id: job.id,
          question: job.question,
        },
      ]);
    },
    [recentResults, setResultResults]
  );
  useEffect(() => {
    if (jobState && recentResults !== null) {
      addRecent(jobState);
    }
  }, [jobState, addRecent, recentResults]);

  return (
    <VStack spacing={10}>
      <Text fontSize={'3rem'}>{jobState?.question}</Text>
      {jobState?.result_probability && (
        <Text
          fontSize={'3rem'}
          color={probabilityFormat(jobState.result_probability / 100)[1]}
        >
          <b>{probabilityFormat(jobState.result_probability / 100)[0]}</b>
        </Text>
      )}
      {(jobState === null || jobState.state === 'pending') && (
        <VStack spacing={7}>
          <Text>Waiting to start</Text>
          <Spinner size="xl" />
        </VStack>
      )}
      {jobState?.state === 'running' && (
        <VStack spacing={7}>
          <Text>Running (~ 5 mins)</Text>
          <Spinner size="xl" />
          {jobState.logs.length > 0 && (
            <Alert status="info" w={'70vw'} maxW={'800px'}>
              <AlertIcon />
              <AlertDescription>{jobState.logs.at(-1)}</AlertDescription>
            </Alert>
          )}
        </VStack>
      )}
      {jobState?.state === 'error' && (
        <Alert status="error" w={'70vw'} maxW={'800px'}>
          <AlertIcon />
          <AlertDescription>{jobState.error_message}</AlertDescription>
        </Alert>
      )}
      <FixedLikelihoodSlider p={jobState?.result_probability} />
      <Stack spacing={4} paddingTop="40px">
        <Button href="" rightIcon={<PlusSquareIcon />} variant="outline">
          <Link href="/">Make another prediction</Link>
        </Button>
        <AnalysisModalButton job={jobState} />
        <ShareModalButton job={jobState} />
      </Stack>
    </VStack>
  );
}

function FixedLikelihoodSlider({ p }) {
  const labelStyles = {
    mt: '2',
    ml: '-2.5',
    fontSize: 'sm',
  };
  const color = p == null ? 'gray.50' : probabilityFormat(p / 100)[1];
  return (
    <Slider value={p} defaultValue={p}>
      <SliderMark value={25} {...labelStyles}>
        25%
      </SliderMark>
      <SliderMark value={50} {...labelStyles}>
        50%
      </SliderMark>
      <SliderMark value={75} {...labelStyles}>
        75%
      </SliderMark>
      {/* {p !== null && (
        <SliderMark value={p} textAlign="center" mt="-10" ml="-5" w="12">
          {p}%
        </SliderMark>
      )} */}
      <SliderTrack bg={color}></SliderTrack>
      {p !== null && <SliderThumb />}
    </Slider>
  );
}

function AnalysisModalButton({ job }) {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <>
      <Button onClick={onOpen} rightIcon={<ChatIcon />} variant="outline">
        Analysis
      </Button>

      <Modal onClose={onClose} isOpen={isOpen} isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{job?.question}</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack>
              {job?.error_message && <Text>{job.error_message}</Text>}
              {(job?.logs || []).map(log => (
                <Text key={log}>{log}</Text>
              ))}
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button onClick={onClose}>Close</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}

function ShareModalButton({ job }) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const shareURL = `https://oracle.sshh.io/results/${job?.id}`;

  return (
    <>
      <Button
        onClick={onOpen}
        rightIcon={<ExternalLinkIcon />}
        colorScheme="teal"
        variant="solid"
      >
        Share Prediction
      </Button>

      <Modal onClose={onClose} isOpen={isOpen} isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Share</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Stack direction="row">
              <TwitterShareButton url={shareURL}>
                <TwitterIcon size={32} round />
              </TwitterShareButton>
              <RedditShareButton url={shareURL}>
                <RedditIcon size={32} round />
              </RedditShareButton>
              <FacebookShareButton url={shareURL}>
                <FacebookIcon size={32} round />
              </FacebookShareButton>
              <LinkedinShareButton url={shareURL}>
                <LinkedinIcon size={32} round />
              </LinkedinShareButton>
            </Stack>
          </ModalBody>
          <ModalFooter>
            <Button onClick={onClose}>Close</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}

export default Result;
