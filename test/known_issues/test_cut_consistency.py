from tempfile import TemporaryDirectory

import pytest

from lhotse import Fbank, LilcomFilesWriter
from test.known_issues.utils import make_cut


@pytest.mark.parametrize(
    ['sampling_rate', 'num_samples'],
    [
        (16000, 15995),
        (16000, 15996),
        (16000, 15997),
        (16000, 15998),
        (16000, 15999),
        (16000, 16000),
        (16000, 16001),
        (16000, 16002),
        (16000, 16003),
        (16000, 16004),
        (16000, 16005),
    ]
)
def test_simple_cut_num_frames_and_samples_are_consistent(sampling_rate, num_samples):
    with make_cut(sampling_rate, num_samples) as cut, \
            TemporaryDirectory() as dir, \
            LilcomFilesWriter(dir) as storage:
        cut = cut.compute_and_store_features(
            extractor=Fbank(),
            storage=storage
        )
        feats = cut.load_features()
        samples = cut.load_audio()

        assert cut.has_features
        assert feats.shape[0] == cut.features.num_frames
        assert feats.shape[0] == cut.num_frames
        assert feats.shape[1] == cut.features.num_features
        assert feats.shape[1] == cut.num_features

        assert cut.has_recording
        assert samples.shape[0] == 1
        assert samples.shape[1] == cut.recording.num_samples
        assert samples.shape[1] == cut.num_samples


@pytest.mark.parametrize(
    ['sampling_rate', 'num_samples', 'padded_duration'],
    [
        (16000, 15995, 1.5),
        (16000, 15996, 1.5),
        (16000, 15997, 1.5),
        (16000, 15998, 1.5),
        (16000, 15999, 1.5),
        (16000, 16000, 1.5),
        (16000, 16001, 1.5),
        (16000, 16002, 1.5),
        (16000, 16003, 1.5),
        (16000, 16004, 1.5),
        (16000, 16005, 1.5),
    ]
)
def test_padded_cut_num_frames_and_samples_are_consistent(sampling_rate, num_samples, padded_duration):
    with make_cut(sampling_rate, num_samples) as cut, \
            TemporaryDirectory() as dir, \
            LilcomFilesWriter(dir) as storage:
        cut = cut.compute_and_store_features(
            extractor=Fbank(),
            storage=storage
        )
        cut = cut.pad(padded_duration)
        feats = cut.load_features()
        samples = cut.load_audio()

        assert cut.has_features
        assert feats.shape[0] == cut.num_frames
        assert feats.shape[1] == cut.num_features

        assert cut.has_recording
        assert samples.shape[0] == 1
        assert samples.shape[1] == cut.num_samples
