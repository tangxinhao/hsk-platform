<template>
  <div class="category-form">
    <el-form :model="form" :rules="rules" ref="categoryForm" label-width="120px">
      <el-form-item label="分类名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入分类名称"></el-input>
      </el-form-item>
      <el-form-item label="描述" prop="description">
        <el-input type="textarea" v-model="form.description" placeholder="请输入分类描述"></el-input>
      </el-form-item>
      <el-form-item label="级别" prop="level">
        <el-select v-model="form.level" placeholder="请选择级别">
          <el-option label="初级" value="初级"></el-option>
          <el-option label="中级" value="中级"></el-option>
          <el-option label="高级" value="高级"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { api } from '@/api';

export default {
  name: 'CategoryForm',
  props: {
    initialData: {
      type: Object,
      default: () => ({
        name: '',
        description: '',
        level: '初级'
      })
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      form: {
        name: this.initialData.name || '',
        description: this.initialData.description || '',
        level: this.initialData.level || '初级'
      },
      rules: {
        name: [
          { required: true, message: '请输入分类名称', trigger: 'blur' },
          { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
        ],
        level: [
          { required: true, message: '请选择级别', trigger: 'change' }
        ]
      }
    };
  },
  methods: {
    submitForm() {
      this.$refs.categoryForm.validate(valid => {
        if (!valid) {
          this.$message.error('请完成必填项');
          return;
        }

        const data = {
          name: this.form.name,
          description: this.form.description,
          level: this.form.level
        };

        console.log('提交分类数据:', data);

        if (this.isEdit && this.initialData.id) {
          // 编辑现有分类
          api.put(`/culture/category/${this.initialData.id}/`, data)
            .then(response => {
              this.$message.success('更新成功');
              this.$emit('success', response.data);
            })
            .catch(error => {
              console.error('更新失败:', error);
              const errorMsg = error.response?.data?.detail || 
                               JSON.stringify(error.response?.data) || 
                               '未知错误';
              this.$message.error(`更新失败: ${errorMsg}`);
            });
        } else {
          // 创建新分类
          api.post('/culture/category/', data)
            .then(response => {
              this.$message.success('创建成功');
              this.resetForm();
              this.$emit('success', response.data);
            })
            .catch(error => {
              console.error('创建失败:', error);
              const errorMsg = error.response?.data?.detail || 
                               JSON.stringify(error.response?.data) || 
                               '未知错误';
              this.$message.error(`创建失败: ${errorMsg}`);
            });
        }
      });
    },
    resetForm() {
      this.$refs.categoryForm.resetFields();
    }
  }
};
</script>

<style scoped>
.category-form {
  max-width: 600px;
  margin: 0 auto;
}
</style> 