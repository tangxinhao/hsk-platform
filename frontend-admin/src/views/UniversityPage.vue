<template>
  <div class="university-container">
    <div class="page-header">
      <h1>高校信息管理</h1>
      <el-button type="primary" @click="openAddDialog">添加高校</el-button>
    </div>

    <div class="search-area">
      <el-input
        v-model="searchQuery"
        placeholder="搜索高校名称"
        prefix-icon="el-icon-search"
        clearable
        @input="handleSearch"
      />
      <el-select v-model="filterRegion" placeholder="按地区筛选" @change="handleSearch">
        <el-option label="全部地区" value=""></el-option>
        <el-option
          v-for="region in regions"
          :key="region"
          :label="region"
          :value="region"
        ></el-option>
      </el-select>
      <el-select v-model="filter985" placeholder="985工程" @change="handleSearch">
        <el-option label="全部" value=""></el-option>
        <el-option label="是" value="true"></el-option>
        <el-option label="否" value="false"></el-option>
      </el-select>
      <el-select v-model="filter211" placeholder="211工程" @change="handleSearch">
        <el-option label="全部" value=""></el-option>
        <el-option label="是" value="true"></el-option>
        <el-option label="否" value="false"></el-option>
      </el-select>
    </div>

    <div class="table-container">
      <el-table
        :data="filteredUniversities"
        stripe
        border
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="name" label="高校名称" width="180" />
        <el-table-column prop="region" label="所在地区" width="100" />
        <el-table-column label="学费(元/年)" width="130" align="right">
          <template v-slot="scope">
            <span v-if="scope.row.tuition_fee" style="color: #fa8c16; font-weight: bold;">
              ¥{{ scope.row.tuition_fee.toLocaleString() }}
            </span>
            <span v-else style="color: #999;">-</span>
          </template>
        </el-table-column>
        <el-table-column label="HSK要求" width="100" align="center">
          <template v-slot="scope">
            <el-tag v-if="scope.row.min_hsk_level" type="warning" size="small">
              HSK {{ scope.row.min_hsk_level }}
            </el-tag>
            <span v-else style="color: #999;">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="establishYear" label="建校时间" width="100" />
        <el-table-column prop="website" label="官网" min-width="150">
          <template v-slot="scope">
            <a :href="scope.row.website" target="_blank" style="font-size: 12px;">{{ scope.row.website }}</a>
          </template>
        </el-table-column>
        <el-table-column label="985工程" width="80" align="center">
          <template v-slot="scope">
            <el-tag v-if="scope.row.is985" type="success" size="small">是</el-tag>
            <el-tag v-else type="info" size="small">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="211工程" width="80" align="center">
          <template v-slot="scope">
            <el-tag v-if="scope.row.is211" type="success" size="small">是</el-tag>
            <el-tag v-else type="info" size="small">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="双一流" width="80" align="center">
          <template v-slot="scope">
            <el-tag v-if="scope.row.isDoubleFirstClass" type="success" size="small">是</el-tag>
            <el-tag v-else type="info" size="small">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="160">
          <template v-slot="scope">
            <span style="font-size: 12px;">{{ formatDateTime(scope.row.createdAt) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template v-slot="scope">
            <el-button size="small" type="primary" @click="editUniversity(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="confirmDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalUniversities"
        ></el-pagination>
      </div>
    </div>

    <!-- 添加/编辑大学对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="50%">
      <el-form :model="universityForm" :rules="rules" ref="universityForm" label-width="120px">
        <el-form-item label="高校名称" prop="name">
          <el-input v-model="universityForm.name" placeholder="请输入高校名称"></el-input>
        </el-form-item>
        <el-form-item label="英文名称" prop="englishName">
          <el-input v-model="universityForm.englishName" placeholder="请输入英文名称"></el-input>
        </el-form-item>
        <el-form-item label="所在地区" prop="region">
          <el-select v-model="universityForm.region" placeholder="请选择地区" style="width: 100%">
            <el-option
              v-for="region in regions"
              :key="region"
              :label="region"
              :value="region"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="建校时间" prop="establishYear">
          <el-input-number v-model="universityForm.establishYear" :min="1000" :max="2100"></el-input-number>
        </el-form-item>
        <el-form-item label="官网" prop="website">
          <el-input v-model="universityForm.website" placeholder="请输入官网地址"></el-input>
        </el-form-item>
        <el-form-item label="排名" prop="ranking">
          <el-input-number v-model="universityForm.ranking" :min="1" :max="1000"></el-input-number>
        </el-form-item>
        
        <el-divider content-position="left">入学要求</el-divider>
        
        <el-form-item label="HSK等级要求">
          <el-select v-model="universityForm.min_hsk_level" placeholder="请选择HSK等级" style="width: 100%">
            <el-option label="HSK 1" :value="1"></el-option>
            <el-option label="HSK 2" :value="2"></el-option>
            <el-option label="HSK 3" :value="3"></el-option>
            <el-option label="HSK 4" :value="4"></el-option>
            <el-option label="HSK 5" :value="5"></el-option>
            <el-option label="HSK 6" :value="6"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="学费(元/年)" prop="tuition_fee">
          <el-input-number 
            v-model="universityForm.tuition_fee" 
            :min="0" 
            :max="100000" 
            :step="1000"
            placeholder="请输入学费"
            style="width: 100%"
          ></el-input-number>
          <div style="color: #909399; font-size: 12px; margin-top: 5px;">
            参考：文科约20,000-25,000元，理工科约25,000-30,000元
          </div>
        </el-form-item>
        
        <el-form-item label="语言要求">
          <el-input 
            v-model="universityForm.language_requirements" 
            placeholder="例如：HSK 5级及以上，部分专业要求6级"
            type="textarea"
            rows="2"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="奖学金信息">
          <el-input 
            v-model="universityForm.scholarship" 
            placeholder="例如：中国政府奖学金、大学国际学生奖学金"
            type="textarea"
            rows="2"
          ></el-input>
        </el-form-item>
        
        <el-divider content-position="left">学校标签</el-divider>
        
        <el-form-item label="985工程">
          <el-switch v-model="universityForm.is985"></el-switch>
        </el-form-item>
        <el-form-item label="211工程">
          <el-switch v-model="universityForm.is211"></el-switch>
        </el-form-item>
        <el-form-item label="双一流">
          <el-switch v-model="universityForm.isDoubleFirstClass"></el-switch>
        </el-form-item>
        
        <el-divider content-position="left">学校介绍</el-divider>
        
        <el-form-item label="简介" prop="description">
          <el-input type="textarea" v-model="universityForm.description" rows="4"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitUniversity" :loading="submitLoading">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { apiService } from '../api/index.js'
import { formatDateTime } from '../utils/dateFormatter.js'

export default {
  name: 'UniversityPage',
  data() {
    return {
      universities: [],
      filteredUniversities: [],
      loading: false,
      submitLoading: false,
      dialogVisible: false,
      dialogTitle: '添加高校',
      isEditing: false,
      universityForm: {
        name: '',
        englishName: '',
        region: '',
        establishYear: new Date().getFullYear(),
        website: '',
        ranking: 1,
        min_hsk_level: 5,
        tuition_fee: null,
        language_requirements: '',
        scholarship: '',
        is985: false,
        is211: false,
        isDoubleFirstClass: false,
        description: ''
      },
      rules: {
        name: [{ required: true, message: '请输入高校名称', trigger: 'blur' }],
        englishName: [{ required: true, message: '请输入英文名称', trigger: 'blur' }],
        region: [{ required: true, message: '请选择所在地区', trigger: 'change' }],
        website: [
          { required: true, message: '请输入官网地址', trigger: 'blur' },
          { type: 'url', message: '请输入有效的URL地址', trigger: 'blur' }
        ]
      },
      regions: [
        '北京', '上海', '广东', '江苏', '浙江', '四川', '湖北', '湖南', 
        '河北', '河南', '山东', '山西', '陕西', '安徽', '福建', '江西', 
        '广西', '云南', '贵州', '辽宁', '吉林', '黑龙江', '内蒙古', 
        '新疆', '西藏', '宁夏', '甘肃', '青海', '天津', '重庆', '海南'
      ],
      searchQuery: '',
      filterRegion: '',
      filter985: '',
      filter211: '',
      currentPage: 1,
      pageSize: 10,
      totalUniversities: 0
    };
  },
  created() {
    this.fetchUniversities();
  },
  methods: {
    formatDateTime,
    fetchUniversities() {
      this.loading = true;
      apiService.getUniversities({ page_size: 10000 })
        .then(response => {
          console.log('获取高校列表:', response);
          if (response.data && response.data.results) {
            this.universities = response.data.results;
          } else if (Array.isArray(response.data)) {
            this.universities = response.data;
          } else {
            this.universities = [];
          }
          console.log(`成功加载 ${this.universities.length} 所大学`);
          this.applyFilters();
        })
        .catch(error => {
          console.error('获取高校列表失败:', error);
          this.$message.error('获取高校列表失败');
        })
        .finally(() => {
          this.loading = false;
        });
    },
    applyFilters() {
      // 确保universities是数组
      if (!Array.isArray(this.universities)) {
        this.universities = [];
        this.filteredUniversities = [];
        this.totalUniversities = 0;
        return;
      }
      
      // 初始化filtered变量
      let filtered = [...this.universities];
      
      // 应用搜索过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(uni => 
          uni.name.toLowerCase().includes(query) || 
          (uni.englishName && uni.englishName.toLowerCase().includes(query))
        );
      }
      
      // 应用地区过滤
      if (this.filterRegion) {
        filtered = filtered.filter(uni => uni.region === this.filterRegion);
      }
      
      // 应用985过滤
      if (this.filter985 !== '') {
        const is985 = this.filter985 === 'true';
        filtered = filtered.filter(uni => uni.is985 === is985);
      }
      
      // 应用211过滤
      if (this.filter211 !== '') {
        const is211 = this.filter211 === 'true';
        filtered = filtered.filter(uni => uni.is211 === is211);
      }
      
      this.totalUniversities = filtered.length;
      
      // 应用分页
      const startIndex = (this.currentPage - 1) * this.pageSize;
      this.filteredUniversities = filtered.slice(startIndex, startIndex + this.pageSize);
    },
    handleSearch() {
      this.currentPage = 1;
      this.applyFilters();
    },
    handleSizeChange(size) {
      this.pageSize = size;
      this.applyFilters();
    },
    handleCurrentChange(page) {
      this.currentPage = page;
      this.applyFilters();
    },
    openAddDialog() {
      this.isEditing = false;
      this.dialogTitle = '添加高校';
      this.universityForm = {
        name: '',
        englishName: '',
        region: '',
        establishYear: new Date().getFullYear(),
        website: '',
        ranking: 1,
        min_hsk_level: 5,
        tuition_fee: null,
        language_requirements: '',
        scholarship: '',
        is985: false,
        is211: false,
        isDoubleFirstClass: false,
        description: ''
      };
      this.dialogVisible = true;
      
      // 确保表单验证重置
      this.$nextTick(() => {
        if (this.$refs.universityForm) {
          this.$refs.universityForm.clearValidate();
        }
      });
    },
    editUniversity(university) {
      console.log('编辑高校:', university);
      this.isEditing = true;
      this.dialogTitle = '编辑高校';
      // 创建一个深拷贝以避免直接修改原始对象
      this.universityForm = JSON.parse(JSON.stringify(university));
      this.dialogVisible = true;
      
      // 确保表单验证重置
      this.$nextTick(() => {
        if (this.$refs.universityForm) {
          this.$refs.universityForm.clearValidate();
        }
      });
    },
    submitUniversity() {
      this.$refs.universityForm.validate(valid => {
        if (!valid) {
          return;
        }
        
        this.submitLoading = true;
        
        const savePromise = this.isEditing
          ? apiService.updateUniversity(this.universityForm.id, this.universityForm)
          : apiService.createUniversity(this.universityForm);
          
        savePromise
          .then(response => {
            console.log('保存高校成功:', response);
            this.$message.success(this.isEditing ? '高校更新成功' : '高校添加成功');
            this.dialogVisible = false;
            this.fetchUniversities();
          })
          .catch(error => {
            console.error('保存高校失败:', error);
            this.$message.error('保存失败: ' + (error.response?.data?.message || error.message));
          })
          .finally(() => {
            this.submitLoading = false;
          });
      });
    },
    confirmDelete(university) {
      this.$confirm(`确定要删除「${university.name}」吗?`, '警告', {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(() => {
        this.loading = true;
        apiService.deleteUniversity(university.id)
          .then(() => {
            this.$message.success('高校删除成功');
            this.fetchUniversities();
          })
          .catch(error => {
            console.error('删除高校失败:', error);
            this.$message.error('删除失败: ' + (error.response?.data?.message || error.message));
          })
          .finally(() => {
            this.loading = false;
          });
      }).catch(() => {
        // 用户取消删除
      });
    }
  }
}
</script>

<style scoped>
.university-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-area {
  display: flex;
  margin-bottom: 20px;
  gap: 15px;
}

.search-area .el-input {
  width: 250px;
}

.table-container {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style> 