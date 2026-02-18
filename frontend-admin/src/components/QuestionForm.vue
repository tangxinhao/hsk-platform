<template>
  <el-form :model="formData" :rules="rules" ref="questionForm" label-width="120px" class="question-form">
    <el-form-item label="题目内容" prop="content">
      <el-input type="textarea" v-model="formData.content" :rows="4" placeholder="请输入题目内容"></el-input>
    </el-form-item>

    <el-form-item label="难度等级" prop="level">
      <el-select v-model="formData.level" placeholder="请选择难度等级">
        <el-option label="1" :value="1"></el-option>
        <el-option label="2" :value="2"></el-option>
        <el-option label="3" :value="3"></el-option>
        <el-option label="4" :value="4"></el-option>
        <el-option label="5" :value="5"></el-option>
        <el-option label="6" :value="6"></el-option>
      </el-select>
    </el-form-item>

    <el-form-item label="题目类型" prop="type">
      <el-select v-model="formData.type" placeholder="请选择题型">
        <el-option label="单选题" value="单选题"></el-option>
        <el-option label="多选题" value="多选题"></el-option>
        <el-option label="判断题" value="判断题"></el-option>
        <el-option label="填空题" value="填空题"></el-option>
        <el-option label="翻译题" value="翻译题"></el-option>
      </el-select>
    </el-form-item>

    <el-form-item label="图片(可选)">
      <el-upload
        action=""
        list-type="picture-card"
        :auto-upload="false"
        :on-change="handleImageChange"
        :limit="1"
        :file-list="imageList">
        <i slot="default" class="el-icon-plus"></i>
        <div slot="file" slot-scope="{file}">
          <img class="el-upload-list__item-thumbnail" :src="file.url" alt="">
          <span class="el-upload-list__item-actions">
            <span class="el-upload-list__item-delete" @click="handleRemoveImage(file)">
              <i class="el-icon-delete"></i>
            </span>
          </span>
        </div>
      </el-upload>
    </el-form-item>

    <el-form-item label="音频(可选)">
      <el-upload
        action=""
        :auto-upload="false"
        :on-change="handleAudioChange"
        :limit="1"
        :file-list="audioList">
        <el-button size="small" type="primary">选择音频</el-button>
        <div slot="tip" class="el-upload__tip">只能上传mp3/wav文件</div>
      </el-upload>
    </el-form-item>

    <!-- 动态选项 -->
    <template v-if="formData.type === '单选题' || formData.type === '多选题'">
      <div class="options-header">
        <h3>选项</h3>
        <el-button type="text" icon="el-icon-plus" @click="addOption">添加选项</el-button>
      </div>

      <el-form-item 
        v-for="(option, index) in formData.options" 
        :key="index"
        :label="'选项' + optionLabels[index]"
        :prop="'options.' + index + '.content'"
        :rules="{ required: true, message: '选项内容不能为空', trigger: 'blur' }">
        <div class="option-row">
          <el-input v-model="option.content" placeholder="请输入选项内容"></el-input>
          <el-checkbox v-model="option.isCorrect" @change="handleCorrectChange(index)">正确答案</el-checkbox>
          <el-button type="danger" icon="el-icon-delete" circle @click="removeOption(index)" :disabled="formData.options.length <= 2"></el-button>
        </div>
      </el-form-item>
    </template>

    <!-- 判断题答案 -->
    <el-form-item label="正确答案" v-if="formData.type === '判断题'" prop="answer">
      <el-radio-group v-model="formData.answer">
        <el-radio label="true">正确</el-radio>
        <el-radio label="false">错误</el-radio>
      </el-radio-group>
    </el-form-item>

    <!-- 填空题/翻译题答案 -->
    <el-form-item label="标准答案" v-if="formData.type === '填空题' || formData.type === '翻译题'" prop="answer">
      <el-input type="textarea" v-model="formData.answer" :rows="3" placeholder="请输入标准答案"></el-input>
    </el-form-item>

    <el-form-item label="解析(可选)">
      <el-input type="textarea" v-model="formData.explanation" :rows="3" placeholder="请输入题目解析"></el-input>
    </el-form-item>

    <el-form-item label="启用">
      <el-switch v-model="formData.active"></el-switch>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="submitForm" :loading="loading">{{ buttonText }}</el-button>
      <el-button @click="resetForm">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { apiService } from '../api/index.js'

export default {
  name: 'QuestionForm',
  props: {
    initialData: {
      type: Object,
      default: () => ({})
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      formData: {
        content: '',
        level: 1,
        type: '单选题',
        image: null,
        audio: null,
        options: [
          { content: '', isCorrect: false },
          { content: '', isCorrect: false }
        ],
        answer: '',
        explanation: '',
        active: true
      },
      imageList: [],
      audioList: [],
      categoryOptions: [],
      rules: {
        content: [
          { required: true, message: '请输入题目内容', trigger: 'blur' }
        ],
        level: [
          { required: true, message: '请选择难度等级', trigger: 'change' }
        ],
        type: [
          { required: true, message: '请选择题型', trigger: 'change' }
        ],
        answer: [
          { required: true, message: '请输入答案', trigger: 'blur' }
        ]
      },
      optionLabels: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    };
  },
  computed: {
    buttonText() {
      return this.isEdit ? '更新题目' : '添加题目';
    }
  },
  watch: {
    initialData: {
      handler(newVal) {
        if (newVal && Object.keys(newVal).length > 0) {
          this.initForm();
        }
      },
      immediate: true
    },
    'formData.type': function(newVal) {
      this.$nextTick(() => {
        // 重置某些字段，根据题型设置不同的默认值
        if (newVal === '单选题' || newVal === '多选题') {
          if (!this.formData.options || this.formData.options.length < 2) {
            this.formData.options = [
              { content: '', isCorrect: false },
              { content: '', isCorrect: false }
            ];
          }
          this.formData.answer = '';
        } else if (newVal === '判断题') {
          this.formData.options = [];
          this.formData.answer = 'true';
        } else {
          this.formData.options = [];
          this.formData.answer = '';
        }
      });
    }
  },
  created() {
    this.fetchCategories();
  },
  methods: {
    initForm() {
      const data = { ...this.initialData };
      
      // 处理选项数据
      if (data.options && Array.isArray(data.options)) {
        data.options = JSON.parse(JSON.stringify(data.options)); // 深拷贝
      } else if (data.type === '单选题' || data.type === '多选题') {
        data.options = [
          { content: '', isCorrect: false },
          { content: '', isCorrect: false }
        ];
      }
      
      // 处理图片
      if (data.imageUrl) {
        this.imageList = [{
          name: 'current-image',
          url: data.imageUrl
        }];
      } else {
        this.imageList = [];
      }
      
      // 处理音频
      if (data.audioUrl) {
        this.audioList = [{
          name: 'current-audio',
          url: data.audioUrl
        }];
      } else {
        this.audioList = [];
      }
      
      this.formData = data;
      
      // 确保类别正确初始化
      if (typeof data.category === 'string') {
        try {
          this.formData.category = data.category.split(',');
        } catch (err) {
          this.formData.category = [];
          console.error('Category parsing error:', err);
        }
      } else if (!data.category) {
        this.formData.category = [];
      }
    },
    fetchCategories() {
      apiService.getCategories()
        .then(response => {
          this.processCategories(response.data);
        })
        .catch(error => {
          console.error('获取分类失败:', error);
          this.$message.error('获取分类失败');
        });
    },
    processCategories(categories) {
      const options = [];
      
      // 按级别分组
      const levelGroups = {};
      categories.forEach(cat => {
        if (!levelGroups[cat.level]) {
          levelGroups[cat.level] = [];
        }
        levelGroups[cat.level].push(cat);
      });
      
      // 构建级联选择器数据结构
      Object.keys(levelGroups).forEach(level => {
        const levelOption = {
          value: level,
          label: level,
          children: levelGroups[level].map(cat => ({
            value: cat.id.toString(),
            label: cat.name
          }))
        };
        options.push(levelOption);
      });
      
      this.categoryOptions = options;
    },
    addOption() {
      if (this.formData.options.length < 8) {
        this.formData.options.push({ 
          content: '', 
          isCorrect: false 
        });
      } else {
        this.$message.warning('最多只能添加8个选项');
      }
    },
    removeOption(index) {
      if (this.formData.options.length > 2) {
        this.formData.options.splice(index, 1);
      }
    },
    handleCorrectChange(changedIndex) {
      // 如果是单选题，确保只有一个正确答案
      if (this.formData.type === '单选题') {
        this.formData.options.forEach((option, index) => {
          if (index !== changedIndex) {
            option.isCorrect = false;
          }
        });
      }
      
      // 校验是否有正确答案
      const hasCorrect = this.formData.options.some(option => option.isCorrect);
      if (!hasCorrect && this.formData.options[changedIndex].isCorrect === false) {
        this.$message.warning('请至少选择一个正确答案');
        this.formData.options[changedIndex].isCorrect = true;
      }
    },
    handleImageChange(file) {
      const isImage = file.raw.type.indexOf('image/') !== -1;
      if (!isImage) {
        this.$message.error('请上传图片文件!');
        this.imageList = [];
        return false;
      }
      
      this.formData.image = file.raw;
      this.imageList = [file];
    },
    handleAudioChange(file) {
      const isAudio = file.raw.type.indexOf('audio/') !== -1;
      if (!isAudio) {
        this.$message.error('请上传音频文件!');
        this.audioList = [];
        return false;
      }
      
      this.formData.audio = file.raw;
      this.audioList = [file];
    },
    handleRemoveImage() {
      this.imageList = [];
      this.formData.image = null;
    },
    submitForm() {
      this.$refs.questionForm.validate(valid => {
        if (!valid) {
          return false;
        }
        
        // 根据题型处理答案和选项
        let answer = '';
        let options = '';
        
        if (this.formData.type === '单选题' || this.formData.type === '多选题') {
          // 验证选项
          if (this.formData.options.length < 2) {
            this.$message.error('请至少添加两个选项');
            return false;
          }
          
          // 验证是否有正确答案
          const correctOptions = this.formData.options.filter(opt => opt.isCorrect);
          if (correctOptions.length === 0) {
            this.$message.error('请至少选择一个正确答案');
            return false;
          }
          
          // 单选题只能有一个正确答案
          if (this.formData.type === '单选题' && correctOptions.length > 1) {
            this.$message.error('单选题只能有一个正确答案');
            return false;
          }
          
          // 设置选项JSON字符串
          options = JSON.stringify(this.formData.options);
          
          // 设置答案：对于单选题和多选题，答案是正确的选项内容
          if (this.formData.type === '单选题') {
            answer = correctOptions[0].content;
          } else {
            // 多选题：答案用逗号分隔的多个正确选项内容
            answer = correctOptions.map(opt => opt.content).join(',');
          }
        } else if (this.formData.type === '判断题') {
          answer = this.formData.answer;
          options = ''; // 判断题没有选项
        } else {
          // 填空题和翻译题
          answer = this.formData.answer;
          options = '';
        }
        
        // 准备表单数据
        let formDataToSubmit = new FormData();
        
        // 添加基本字段
        formDataToSubmit.append('content', this.formData.content);
        formDataToSubmit.append('level', this.formData.level);
        formDataToSubmit.append('type', this.formData.type);
        formDataToSubmit.append('answer', answer);
        formDataToSubmit.append('options', options);
        
        // 添加可选字段
        if (this.formData.explanation) {
          formDataToSubmit.append('explanation', this.formData.explanation);
        }
        
        // 添加文件
        if (this.formData.image) {
          formDataToSubmit.append('image', this.formData.image);
        }
        
        if (this.formData.audio) {
          formDataToSubmit.append('audio', this.formData.audio);
        }
        
        console.log('提交题目数据:', {
          content: this.formData.content,
          level: this.formData.level,
          type: this.formData.type,
          answer: answer,
          options: options,
          explanation: this.formData.explanation
        });
        
        this.$emit('submit', formDataToSubmit);
      });
    },
    resetForm() {
      this.$refs.questionForm.resetFields();
      this.imageList = [];
      this.audioList = [];
      
      // 重置为默认值
      this.formData = {
        content: '',
        level: 1,
        type: '单选题',
        image: null,
        audio: null,
        options: [
          { content: '', isCorrect: false },
          { content: '', isCorrect: false }
        ],
        answer: '',
        explanation: '',
        active: true
      };
    }
  }
}
</script>

<style scoped>
.question-form {
  max-width: 800px;
  margin: 0 auto;
}

.options-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.option-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.option-row .el-input {
  flex-grow: 1;
}

.el-upload__tip {
  line-height: 1.2;
  margin-top: 5px;
  font-size: 12px;
}
</style>
