import React, { useState, useEffect } from 'react';
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
} from '@chakra-ui/react';
import { SliderThumb } from '@chakra-ui/react';
import { ExternalLinkIcon, EditIcon } from '@chakra-ui/icons';

function Result() {
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setInterval(() => {
      setLoading(false);
    }, 2000);
  }, []);
  return (
    <VStack spacing={10}>
      <Text fontSize={'5rem'}>Will the world end in 2025?</Text>
      {!loading && (
        <Text fontSize={'2rem'} color="green.500">
          <b>Somewhat Likely</b>
        </Text>
      )}
      {loading && <Spinner size="xl" />}
      <FixedLikelihoodSlider p={loading ? null : 67} />
      <Stack direction="row" spacing={4} paddingTop="40px">
        <Button href="" rightIcon={<EditIcon />} variant="outline">
          <Link href="/">Make another prediction</Link>
        </Button>
        <Button
          rightIcon={<ExternalLinkIcon />}
          colorScheme="teal"
          variant="solid"
        >
          Share Prediction
        </Button>
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
  const color = p == null ? 'gray.50' : 'green.500';
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
      {p !== null && (
        <SliderMark value={p} textAlign="center" mt="-10" ml="-5" w="12">
          {p}%
        </SliderMark>
      )}
      <SliderTrack bg={color}></SliderTrack>
      {p !== null && <SliderThumb />}
    </Slider>
  );
}

export default Result;
