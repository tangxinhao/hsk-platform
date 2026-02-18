<template>
  <div class="category-page">
    <h1>分类管理</h1>
    
    <!-- 创建分类表单 -->
    <div class="create-form">
      <h2>创建新分类</h2>
      <el-form :model="newCategory" label-width="100px">
        <el-form-item label="分类名称" required>
          <el-input v-model="newCategory.name" placeholder="请输入分类名称"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input type="textarea" v-model="newCategory.description" placeholder="请输入描述"></el-input>
        </el-form-item>
        <el-form-item label="级别" required>
          <el-select v-model="newCategory.level" placeholder="请选择级别">
            <el-option label="初级" value="初级"></el-option>
            <el-option label="中级" value="中级"></el-option>
            <el-option label="高级" value="高级"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="createCategory">创建</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 分类列表 -->
    <div class="category-list">
      <h2>分类列表</h2>
      <el-table :data="categories" style="width: 100%">
        <el-table-column prop="id" label="ID" width="50"></el-table-column>
        <el-table-column prop="name" label="分类名称"></el-table-column>
        <el-table-column prop="description" label="描述"></el-table-column>
        <el-table-column prop="level" label="级别"></el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="editCategory(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteCategory(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    
    <!-- 编辑分类对话框 -->
    <el-dialog title="编辑分类" v-model="dialogVisible">
      <el-form :model="editingCategory" label-width="100px">
        <el-form-item label="分类名称" required>
          <el-input v-model="editingCategory.name" placeholder="请输入分类名称"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input type="textarea" v-model="editingCategory.description" placeholder="请输入描述"></el-input>
        </el-form-item>
        <el-form-item label="级别" required>
          <el-select v-model="editingCategory.level" placeholder="请选择级别">
            <el-option label="初级" value="初级"></el-option>
            <el-option label="中级" value="中级"></el-option>
            <el-option label="高级" value="高级"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="updateCategory">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import api from '../api/index';
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  data() {
    return {
      categories: [],
      newCategory: {
        name: '',
        description: '',
        level: '初级'  // 确保默认值是有效的选项
      },
      dialogVisible: false,
      editingCategory: {
        id: null,
        name: '',
        description: '',
        level: '初级'  // 确保默认值是有效的选项
      }
    };
  },
  created() {
    this.loadCategories();
  },
  methods: {
    loadCategories() {
      api.culture.getCategories()
        .then(response => {
          this.categories = response.data.results || response.data;
        })
        .catch(error => {
          console.error('获取分类列表错误:', error);
          ElMessage.error('获取分类列表失败');
        });
    },
    createCategory() {
      console.log('提交的分类数据:', this.newCategory);
      
      if (!this.newCategory.name) {
        ElMessage.error('分类名称不能为空');
        return;
      }
      
      if (!this.newCategory.level) {
        ElMessage.error('请选择级别');
        return;
      }
      
      // 确保level的值是后端可接受的
      if (!['初级', '中级', '高级'].includes(this.newCategory.level)) {
        ElMessage.error('级别必须是初级、中级或高级');
        return;
      }
      
      const categoryData = {
        name: this.newCategory.name,
        description: this.newCategory.description || '',
        level: this.newCategory.level  // 确保这是后端可接受的值
      };
      
      console.log('发送到后端的数据:', categoryData);
      
      api.culture.createCategory(categoryData)
        .then(response => {
          ElMessage.success('创建分类成功');
          this.loadCategories();
          this.resetForm();
        })
        .catch(error => {
          console.error('创建分类错误:', error);
          const errorMsg = error.response?.data?.detail || 
                          JSON.stringify(error.response?.data) || 
                          '未知错误';
          ElMessage.error('创建分类失败: ' + errorMsg);
        });
    },
    editCategory(category) {
      this.editingCategory = { ...category };
      this.dialogVisible = true;
    },
    updateCategory() {
      if (!this.editingCategory.name) {
        ElMessage.error('分类名称不能为空');
        return;
      }
      
      if (!this.editingCategory.level) {
        ElMessage.error('请选择级别');
        return;
      }
      
      // 确保level的值是后端可接受的
      if (!['初级', '中级', '高级'].includes(this.editingCategory.level)) {
        ElMessage.error('级别必须是初级、中级或高级');
        return;
      }
      
      api.culture.updateCategory(this.editingCategory.id, this.editingCategory)
        .then(response => {
          ElMessage.success('更新分类成功');
          this.dialogVisible = false;
          this.loadCategories();
        })
        .catch(error => {
          console.error('更新分类错误:', error);
          const errorMsg = error.response?.data?.detail || 
                          JSON.stringify(error.response?.data) || 
                          '未知错误';
          ElMessage.error('更新分类失败: ' + errorMsg);
        });
    },
    deleteCategory(id) {
      ElMessageBox.confirm('确定要删除这个分类吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        api.culture.deleteCategory(id)
          .then(response => {
            ElMessage.success('删除分类成功');
            this.loadCategories();
          })
          .catch(error => {
            console.error('删除分类错误:', error);
            ElMessage.error('删除分类失败');
          });
      }).catch(() => {
        // 取消删除
      });
    },
    resetForm() {
      this.newCategory = {
        name: '',
        description: '',
        level: '初级'  // 重置为有效的默认选项
      };
    }
  }
};
</script>

<style scoped>
.category-page {
  padding: 20px;
}

.create-form, .category-list {
  margin-bottom: 30px;
}

h1 {
  margin-bottom: 20px;
}

h2 {
  margin-bottom: 15px;
}
</style> 