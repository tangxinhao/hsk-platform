<template>
  <div class="audio-player-wrapper">
    <div class="audio-player" :class="{ 'playing': isPlaying, 'error': hasError }">
      <!-- 播放/暂停按钮 -->
      <button class="play-button" @click="togglePlay" :disabled="hasError">
        <div class="play-icon" v-if="!isPlaying && !hasError">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M8 5v14l11-7z"/>
          </svg>
        </div>
        <div class="pause-icon" v-else-if="isPlaying">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
          </svg>
        </div>
        <div class="error-icon" v-else>
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
          </svg>
        </div>
      </button>
      
      <!-- 进度条 -->
      <div class="progress-container">
        <div class="audio-info">
          <span class="audio-label">
            <svg class="audio-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 3v9.28c-.47-.17-.97-.28-1.5-.28C8.01 12 6 14.01 6 16.5S8.01 21 10.5 21c2.31 0 4.2-1.75 4.45-4H15V6h4V3h-7z"/>
            </svg>
            音频播放器
          </span>
          <span class="time-display">{{ currentTimeFormatted }} / {{ durationFormatted }}</span>
        </div>
        
        <div class="progress-bar" @click="seek" ref="progressBar">
          <div class="progress-track">
            <div class="progress-fill" :style="{ width: progress + '%' }">
              <div class="progress-thumb"></div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 音量控制 -->
      <div class="volume-control">
        <button class="volume-button" @click="toggleMute">
          <svg v-if="volume > 0.5" class="volume-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
          </svg>
          <svg v-else-if="volume > 0" class="volume-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M7 9v6h4l5 5V4l-5 5H7z"/>
          </svg>
          <svg v-else class="volume-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>
          </svg>
        </button>
        <input 
          type="range" 
          min="0" 
          max="100" 
          v-model.number="volumeSlider" 
          @input="updateVolume"
          class="volume-slider"
        />
      </div>
      
      <!-- 下载按钮 -->
      <a 
        v-if="audioUrl && !hasError" 
        :href="audioUrl" 
        download 
        class="download-button"
        title="下载音频"
        @click.stop
      >
        <svg class="download-icon" viewBox="0 0 24 24" fill="currentColor">
          <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
        </svg>
      </a>
      
      <!-- 隐藏的audio元素 -->
      <audio 
        ref="audio" 
        :src="audioUrlWithCacheBuster"
        @loadedmetadata="onLoadedMetadata"
        @timeupdate="onTimeUpdate"
        @ended="onEnded"
        @error="onError"
        @canplay="onCanPlay"
        preload="metadata"
      ></audio>
    </div>
    
    <!-- 错误提示 -->
    <div v-if="hasError" class="error-message">
      <svg class="error-icon-small" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
      </svg>
      <span>音频加载失败，请检查文件路径：{{ audioUrl }}</span>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'

export default {
  name: 'AudioPlayer',
  props: {
    audioUrl: {
      type: String,
      required: true
    },
    autoplay: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const audio = ref(null)
    const isPlaying = ref(false)
    const currentTime = ref(0)
    const duration = ref(0)
    const volume = ref(1)
    const volumeSlider = ref(100)
    const progressBar = ref(null)
    const hasError = ref(false)
    
    // 添加缓存破坏参数的音频URL
    const audioUrlWithCacheBuster = computed(() => {
      if (!props.audioUrl) return ''
      const url = new URL(props.audioUrl, window.location.origin)
      url.searchParams.set('t', Date.now())
      return url.toString()
    })
    
    // 格式化时间
    const formatTime = (seconds) => {
      if (isNaN(seconds)) return '0:00'
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins}:${secs.toString().padStart(2, '0')}`
    }
    
    const currentTimeFormatted = computed(() => formatTime(currentTime.value))
    const durationFormatted = computed(() => formatTime(duration.value))
    const progress = computed(() => {
      if (duration.value === 0) return 0
      return (currentTime.value / duration.value) * 100
    })
    
    // 播放/暂停
    const togglePlay = () => {
      if (hasError.value) return
      
      if (isPlaying.value) {
        audio.value.pause()
        isPlaying.value = false
      } else {
        audio.value.play().catch(err => {
          console.error('播放失败:', err)
          hasError.value = true
        })
        isPlaying.value = true
      }
    }
    
    // 跳转进度
    const seek = (event) => {
      if (hasError.value || !audio.value) return
      
      const rect = progressBar.value.getBoundingClientRect()
      const percent = (event.clientX - rect.left) / rect.width
      audio.value.currentTime = percent * duration.value
    }
    
    // 音量控制
    const updateVolume = () => {
      volume.value = volumeSlider.value / 100
      if (audio.value) {
        audio.value.volume = volume.value
      }
    }
    
    const toggleMute = () => {
      if (volume.value > 0) {
        volumeSlider.value = 0
      } else {
        volumeSlider.value = 100
      }
      updateVolume()
    }
    
    // 事件处理
    const onLoadedMetadata = () => {
      duration.value = audio.value.duration
      hasError.value = false
      console.log('音频加载成功, 时长:', duration.value)
    }
    
    const onTimeUpdate = () => {
      currentTime.value = audio.value.currentTime
    }
    
    const onEnded = () => {
      isPlaying.value = false
      currentTime.value = 0
      audio.value.currentTime = 0
    }
    
    const onError = (e) => {
      console.error('音频加载错误:', e)
      console.error('音频URL:', props.audioUrl)
      hasError.value = true
      isPlaying.value = false
    }
    
    const onCanPlay = () => {
      hasError.value = false
      console.log('音频可以播放')
    }
    
    // 监听URL变化
    watch(() => props.audioUrl, () => {
      hasError.value = false
      isPlaying.value = false
      currentTime.value = 0
      duration.value = 0
      
      if (audio.value) {
        audio.value.load()
      }
    })
    
    // 自动播放
    onMounted(() => {
      if (props.autoplay && audio.value) {
        setTimeout(() => {
          audio.value.play().catch(err => {
            console.error('自动播放失败:', err)
          })
        }, 100)
      }
    })
    
    // 清理
    onBeforeUnmount(() => {
      if (audio.value) {
        audio.value.pause()
      }
    })
    
    return {
      audio,
      isPlaying,
      currentTime,
      duration,
      volume,
      volumeSlider,
      progressBar,
      hasError,
      audioUrlWithCacheBuster,
      currentTimeFormatted,
      durationFormatted,
      progress,
      togglePlay,
      seek,
      updateVolume,
      toggleMute,
      onLoadedMetadata,
      onTimeUpdate,
      onEnded,
      onError,
      onCanPlay
    }
  }
}
</script>

<style scoped>
.audio-player-wrapper {
  width: 100%;
}

.audio-player {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.audio-player.playing {
  box-shadow: 0 6px 30px rgba(102, 126, 234, 0.5);
}

.audio-player.error {
  background: linear-gradient(135deg, #f56c6c 0%, #e74c3c 100%);
}

.play-button {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  background: white;
  color: #667eea;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.play-button:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.play-button:active:not(:disabled) {
  transform: scale(0.95);
}

.play-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.play-icon,
.pause-icon,
.error-icon {
  width: 24px;
  height: 24px;
}

.progress-container {
  flex: 1;
  min-width: 0;
}

.audio-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  color: white;
  font-size: 13px;
}

.audio-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
}

.audio-icon {
  width: 16px;
  height: 16px;
}

.time-display {
  font-variant-numeric: tabular-nums;
  opacity: 0.9;
}

.progress-bar {
  width: 100%;
  height: 8px;
  cursor: pointer;
  padding: 4px 0;
}

.progress-track {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  position: relative;
  overflow: visible;
}

.progress-fill {
  height: 100%;
  background: white;
  border-radius: 2px;
  position: relative;
  transition: width 0.1s ease;
}

.progress-thumb {
  position: absolute;
  right: -6px;
  top: 50%;
  transform: translateY(-50%);
  width: 12px;
  height: 12px;
  background: white;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.progress-bar:hover .progress-thumb {
  opacity: 1;
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.volume-button {
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.volume-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.volume-icon {
  width: 20px;
  height: 20px;
}

.volume-slider {
  width: 80px;
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 12px;
  height: 12px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.volume-slider::-moz-range-thumb {
  width: 12px;
  height: 12px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.download-button {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: all 0.2s ease;
}

.download-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.download-icon {
  width: 20px;
  height: 20px;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #fef0f0;
  border: 1px solid #fde2e2;
  border-radius: 8px;
  color: #f56c6c;
  font-size: 13px;
  margin-top: 12px;
}

.error-icon-small {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .audio-player {
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .progress-container {
    flex-basis: 100%;
    order: 3;
  }
  
  .volume-control {
    order: 2;
  }
  
  .volume-slider {
    width: 60px;
  }
}
</style>
