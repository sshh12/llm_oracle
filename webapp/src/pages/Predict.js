import React, { useState, useEffect } from 'react';
import {
  Text,
  Link,
  VStack,
  Stack,
  Flex,
  InputGroup,
  Input,
  IconButton,
  Button,
  FormControl,
  FormLabel,
  Switch,
  Tooltip,
} from '@chakra-ui/react';
import { SearchIcon, ExternalLinkIcon } from '@chakra-ui/icons';
import { useLocalStorage, STRIPE_LINK } from '../lib/api';
import SettingsModal from './../components/SettingsModal';

const PREDICTION_PLACEHOLDERS = [
  'Will the world end by 2050?',
  'Will next year be the hottest year on record?',
  'Will we discover extraterrestrial life within the next decade?',
  'Will there be a major technological breakthrough in the next 5 years?',
  'Will a universal basic income be implemented worldwide by 2040?',
  'Will AI surpass human intelligence by 2030?',
  'Will humans colonize Mars by 2050?',
  'Will there be a cure for cancer within the next 20 years?',
  'Will teleportation become a reality by 2100?',
  'Will climate change be reversed within the next 50 years?',
  'Will we achieve world peace by 2060?',
  'Will the global population reach 10 billion by 2050?',
  'Will we successfully reverse aging within the next 30 years?',
  'Will virtual reality become indistinguishable from reality by 2045?',
  'Will the majority of vehicles be self-driving by 2035?',
];

function Predict({ userId, user }) {
  const [placeholderIdx, setPlaceholderIdx] = useState(
    Math.floor(Math.random() * PREDICTION_PLACEHOLDERS.length)
  );
  const placeholderPrediction = PREDICTION_PLACEHOLDERS[placeholderIdx];
  const [publicVisable, setPublicVisable] = useLocalStorage(
    'oracle:public',
    () => true
  );
  const [modelTemp, setModelTemp] = useLocalStorage(
    'oracle:modelTemp',
    () => 50
  );
  const [useGPT4, setUseGPT4] = useLocalStorage('oracle:usergpt4', () => false);
  const [recentResults, setRecentResults] = useLocalStorage(
    'oracle:recent',
    () => []
  );
  const [q, setQ] = useState('');

  const modelName = useGPT4 ? 'gpt4' : 'gpt3';
  const question = q || placeholderPrediction;
  const predictURL = `/.netlify/functions/predict?q=${window.encodeURIComponent(
    question
  )}&model=${modelName}&temp=${modelTemp}&public=${publicVisable}&userId=${userId}`;

  const onPredict = () => {
    window.location.href = predictURL;
  };

  useEffect(() => {
    const timeout = setTimeout(() => {
      setPlaceholderIdx((placeholderIdx + 1) % PREDICTION_PLACEHOLDERS.length);
    }, 5000);

    return () => {
      clearTimeout(timeout);
    };
  }, [placeholderIdx]);

  if (predictURL)
    return (
      <VStack spacing={7}>
        <Text fontSize={'5rem'}>🔮</Text>
        <Stack spacing={1}>
          <InputGroup w={'60vw'} minWidth={'340px'}>
            <Input
              type="text"
              placeholder={placeholderPrediction}
              value={q}
              onChange={e => setQ(e.target.value)}
              borderRadius={1}
              onKeyUp={e => {
                if (e.key === 'Enter') {
                  onPredict();
                }
              }}
            />
            <IconButton
              onClick={() => onPredict()}
              borderRadius={1}
              colorScheme={'blue'}
              aria-label="Predict"
              icon={<SearchIcon />}
            />
          </InputGroup>
        </Stack>
        <Flex wrap="wrap" justify="center">
          <FormControl display="flex" alignItems="center">
            <FormLabel htmlFor="better-model" mb="0">
              <Tooltip
                label="Use GPT-4 as an agent with the ability to search the internet. Significantly improves detail of results and analysis. Requires paid predictions (uses 10 prediction credits)."
                fontSize="sm"
                mr={2}
              >
                Improve results with GPT-4
              </Tooltip>
            </FormLabel>

            <Switch
              id="better-model"
              isChecked={useGPT4}
              onChange={e => setUseGPT4(e.target.checked)}
            />
          </FormControl>
        </Flex>
        <Flex wrap="wrap" justify="center">
          <Button m={2} rightIcon={<ExternalLinkIcon />} variant="outline">
            <Link href="https://github.com/sshh12/llm_oracle" isExternal>
              How does this work?
            </Link>
          </Button>
          {userId && (
            <Button m={2} rightIcon={<ExternalLinkIcon />} variant="outline">
              <Link
                href={`${STRIPE_LINK}?client_reference_id=oracle:::${userId}`}
                isExternal
              >
                Get predictions ({user?.credits})
              </Link>
            </Button>
          )}
          <SettingsModal
            {...{
              modelTemp,
              setModelTemp,
              publicVisable,
              setPublicVisable,
              setRecentResults,
              userId,
            }}
          />
        </Flex>
        {recentResults && (
          <VStack>
            {recentResults.toReversed().map(v => (
              <Link key={v.id} href={`/results/${v.id}`}>
                <Text fontSize={'1rem'}>
                  <i>{v.question}</i>
                </Text>
              </Link>
            ))}
          </VStack>
        )}
      </VStack>
    );
}

export default Predict;
