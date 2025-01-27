# Copyright (c) OpenMMLab. All rights reserved.
from .builder import AutoModelConfigBuilder
from .default import DefaultModelConfigBuilder


class CogVLMModelConfigBuilder(AutoModelConfigBuilder):

    @classmethod
    def condition(cls, hf_config):
        """config."""
        model_arch = getattr(hf_config, 'architectures', [None])[0]
        return model_arch == 'CogVLMForCausalLM'

    @classmethod
    def build(cls, hf_config, model_path: str = None):
        """build."""
        from lmdeploy.utils import is_bf16_supported
        cfg = DefaultModelConfigBuilder.build(hf_config)
        if getattr(hf_config, 'num_multi_query_heads', None):
            cfg.num_key_value_heads = hf_config.num_multi_query_heads
        cfg.cogvlm_style = True
        torch_dtype = 'bfloat16' if is_bf16_supported() else 'float16'
        hf_config.torch_dtype = torch_dtype
        return cfg
