# coding: utf-8
# !/usr/bin/env python3

"""SoVITS TTS SDK"""

import requests


def tts(text, server_url, ref_audio_path, prompt_text, top_k, top_p, temperature, text_split_method):
    data = {
        "text": text,
        "text_lang": "zh",
        "ref_audio_path": ref_audio_path,
        "aux_ref_audio_paths": [],
        "prompt_text": prompt_text,
        "prompt_lang": "zh",
        "top_k": top_k,
        "top_p": top_p,
        "temperature": temperature,
        "text_split_method": text_split_method,
        "batch_size": 1,
        "batch_threshold": 0.75,
        "split_bucket": True,
        "speed_factor": 1.1,
        "streaming_mode": False,
        "seed": -1,
        "parallel_infer": True,
        "repetition_penalty": 1.35
    }

    url = f"{server_url}/tts"
    res = requests.post(url=url, json=data)
    res.raise_for_status()
    return res.content
