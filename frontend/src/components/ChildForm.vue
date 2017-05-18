<template>
  <form v-on:submit.prevent="submitForm">
    <div v-for="field in raw_form" v-if="validateField(field.field_name).exists" :class="['form-group', field.classes, {'has-error': validateField(field.field_name).has_error}]">
      <div v-if="field.type === 'hidden-input'" style="display: none;" :key="field.key">
        <label>{{ field.label }}</label>
        <input type="text" :name="field.field_name" :value="field.placeholder" readonly>
      </div>
      <label v-else>{{ field.label }}</label>
      <span class="form-group__message" v-if="validateField(field.field_name).is_required"> *</span>
      <div v-if="['alpha-input', 'email-input'].indexOf(field.type) !== -1" :class="['alpha-input', {'input-group': field.value !== undefined && !form_object[field.field_name].activated}]">
        <input type="text" class="form-control" :name="field.field_name" v-model.trim="form_object[field.field_name].value" :placeholder="field.placeholder" v-on:input="touchField(field.field_name)" :key="field.key" :readonly="field.value !== undefined && !form_object[field.field_name].activated">
        <div v-if="field.value !== undefined && !form_object[field.field_name].activated" class="input-group-btn">
          <button type="button" class="btn btn-warning" v-on:click="activateField(field.field_name)">
            Change
          </button>
        </div>
      </div>
      <div v-if="field.type === 'password-input'" :class="['password-input', {'input-group': field.value != undefined && !form_object[field.field_name].activated}]">
        <input type="password" class="form-control" :name="field.field_name" v-model.trim="form_object[field.field_name].value" :placeholder="field.placeholder" v-on:input="touchField(field.field_name)" :key="field.key" :readonly="field.value !== undefined && !form_object[field.field_name].activated">
        <div v-if="field.value !== undefined  && !form_object[field.field_name].activated" class="input-group-btn">
          <button type="button" class="btn btn-warning" v-on:click="activateField(field.field_name)">
            Change
          </button>
        </div>
      </div>
      <div v-else-if="field.type === 'pikaday-input'" class="pikaday-input input-group">
        <input type="text" class="form-control" :name="field.field_name" :placeholder="field.placeholder" :ref="field.field_name" :value="form_object[field.field_name].value" v-on:input="touchField(field.field_name)" :readonly="!form_object[field.field_name].activated" :key="field.key">
        <div class="input-group-btn">
          <button type="button" :ref="field.field_name+'-btn'" :class="['btn', 'btn-default', {'disabled-button': field.value !== undefined && !form_object[field.field_name].activated}]">
            <icon name="calendar"></icon>
          </button>
          <button v-if="field.value !== undefined  && !form_object[field.field_name].activated" type="button" class="btn btn-warning" v-on:click="activateField(field.field_name)">
            Change
          </button>
        </div>
      </div>
      <div v-else-if="field.type === 'multiselect-input'" :class="['multiselect-input', {'input-group': field.value !== undefined  && !form_object[field.field_name].activated}]">
        <multiselect :options="field.multiselect_options" :placeholder="field.placeholder" deselect-label="Remove" select-label="Select" v-model="form_object[field.field_name].value" v-on:input="touchField(field.field_name)" :key="field.key" :disabled="field.value !== undefined && !form_object[field.field_name].activated" :select-label="field.SelectLabel" :deselect-label="field.DeselectLabel"></multiselect>
        <div v-if="field.value !== undefined  && !form_object[field.field_name].activated" class="input-group-btn">
          <button type="button" class="btn btn-warning" v-on:click="activateField(field.field_name)">
          Change
          </button>
        </div>
      </div>
      <div v-else-if="field.type === 'search-input'" :class="['search-input', {'input-group': field.value !== undefined  && !form_object[field.field_name].activated}]">
        <multiselect :options="form_object[field.field_name].options" :placeholder="field.placeholder" :loading="form_object[field.field_name].loading" :options-limit="10" :searchable="true" :internal-search="false" v-on:search-change="asyncFind(field.field_name, $event)" v-model="form_object[field.field_name].value" v-on:input="touchField(field.field_name)" :key="field.key" :disabled="field.value !== undefined && !form_object[field.field_name].activated" :select-label="field.SelectLabel" :deselect-label="field.DeselectLabel">
          <span slot="noResult">Oops! Person not found.</span>
        </multiselect>
        <div v-if="field.value !== undefined  && !form_object[field.field_name].activated" class="input-group-btn">
          <button type="button" class="btn btn-warning" v-on:click="activateField(field.field_name)">
            Change
          </button>
        </div>
      </div>
      <!-- <pre v-if="!!$v.form_object[field.field_name].value">{{$v.form_object[field.field_name].value}}</pre> -->
      <span class="form-group__message" v-if="validateField(field.field_name).failed_required">{{ field.label }} is required</span>
      <span class="form-group__message" v-else-if="validateField(field.field_name).failed_alpha">{{ field.label }} is not valid</span>
      <span class="form-group__message" v-else-if="validateField(field.field_name).failed_email">Invalid email address</span>
    </div>
    <div v-for="field in form_object" v-if="field.type === 'submit-button'" class="form-group__buttons form-group">
      <button type="submit" :class="field.button_class">{{ field.button_message }}</button>
    </div>
  </form>
</template>

<script>
  import { required, email, alpha } from 'vuelidate/lib/validators'
  import { validationMixin } from 'vuelidate'
  import Multiselect from 'vue-multiselect'
  import bus from '@/utils/bus'

  var Pikaday = require('pikaday')

  function extendDict (obj, src) {
    for (var key in src) {
      if (src.hasOwnProperty(key)) {
        obj[key] = src[key]
      }
      return obj
    }
  }

  export default {
    mixins: [validationMixin],
    components: {
      multiselect: Multiselect
    },
    props: {
      raw_form: {
        type: Array,
        required: true
      },
      submit_url: {
        type: String,
        required: true
      },
      search_url: {
        type: String,
        required: true
      }
    },
    data: function () {
      return {
        form_object: this.createFormObject(),
        picker: {}
      }
    },
    validations: function () {
      var validationsDict = { form_object: {} }
      for (var key in this.form_object) {
        validationsDict.form_object[key] = {}
        validationsDict.form_object[key].value = {}
        if (Object.keys(this.form_object[key]).indexOf('validators') !== -1) {
          var validators = this.form_object[key].validators
          validationsDict.form_object[key].value = validators
        }
      }
      return validationsDict
    },
    methods: {
      submitForm: function () {
        if (!this.$v.$invalid) {
          var formData = {}
          for (var field in this.form) {
            formData[field] = this.form[field].value
          }
          // submit form data here
        } else {
          this.$v.$touch()
        }
      },
      asyncFind: function (fieldName, value) {
        this.form_object[fieldName].loading = true
        // Perform full text search here
      },
      createFormObject: function () {
        var processed = {}
        for (var index in this.raw_form) {
          var key = this.raw_form[index].field_name
          if (this.raw_form[index].type !== 'submit-button') {
            processed[key] = {}
            if (this.raw_form[index].type === 'search-input') {
              processed[key]['loading'] = false
              processed[key]['options'] = []
            }
            if (Object.keys(this.raw_form[index]).indexOf('value') !== -1) {
              processed[key]['value'] = this.raw_form[index].value
            } else {
              processed[key]['value'] = ''
            }
            processed[key]['activated'] = false
          }
          if (this.raw_form[index].validators !== undefined) {
            var fieldValidators = this.raw_form[index].validators
            processed[key].validators = {}
            for (var index2 in fieldValidators) {
              if (fieldValidators[index2] === 'required') {
                extendDict(processed[key].validators, { required })
              } else if (fieldValidators[index2] === 'alpha') {
                extendDict(processed[key].validators, { alpha })
              } else if (fieldValidators[index2] === 'email') {
                extendDict(processed[key].validators, { email })
              }
            }
          }
        }
        return processed
      },
      activateField: function (fieldName) {
        this.form_object[fieldName].activated = true
        bus.$emit('form-field-activated')
      },
      validateField: function (fieldName) {
        var validation = {}

        validation.exists = this.$v.form_object[fieldName] !== null
        validation.has_error = this.$v.form_object[fieldName].$error
        validation.is_dirty = this.$v.form_object[fieldName].value.$dirty
        validation.is_required = Object.keys(this.$v.form_object[fieldName].value).indexOf('required') !== -1
        validation.is_alpha = Object.keys(this.$v.form_object[fieldName].value).indexOf('alpha') !== -1
        validation.is_email = Object.keys(this.$v.form_object[fieldName].value).indexOf('email') !== -1
        validation.failed_required = !this.$v.form_object[fieldName].value.required && validation.is_required && validation.is_dirty
        validation.failed_alpha = !this.$v.form_object[fieldName].value.alpha && validation.is_alpha && validation.is_dirty
        validation.failed_email = !this.$v.form_object[fieldName].value.email && validation.is_email && validation.is_dirty

        return validation
      },
      touchField: function (fieldName) {
        this.$v.form_object[fieldName].value.$touch()
        this.activateField(fieldName)
      }
    },
    computed: {
      pikaday_Hooks: function () {
        var hooks = []
        if (Object.keys(this.$refs).length === 2) {
          for (var ref in this.$refs) {
            if (ref.indexOf('-btn') === -1) {
              hooks.push(ref)
            }
            hooks.push(this.$refs[ref])
          }
        } else {
          return null
        }
        return hooks
      }
    },
    mounted: function () {
      var self = this
      if (this.pikaday_Hooks) {
        for (var index in this.pikaday_Hooks) {
          if (typeof this.pikaday_Hooks[index] === 'string') {
            var pikadayFieldName = this.pikaday_Hooks[index]
            this.pikaday_Hooks.splice(index, 1)
          }
        }
        this.picker = new Pikaday({
          ref: this.base_ref,
          field: this.pikaday_Hooks[0][0],
          trigger: this.pikaday_Hooks[1][0],
          onSelect: function () {
            var date = this.getMoment().format('Do MMMM YYYY')
            self.form_object[pikadayFieldName].value = date
            self.activateField(pikadayFieldName)
          }
        })
      }
    }
  }
</script>

<style scoped>
  @import '../../node_modules/pikaday/css/pikaday.css';
  @import '../../node_modules/vue-multiselect/dist/vue-multiselect.min.css';
  label {
    font-size: 15px;
    font-weight: 600
  }
  .form-control {
    margin-bottom: 2px;
    border-radius: 5px;
    border: 1px solid rgba(232, 232, 232, 1);
    min-height: 40px;
    box-shadow: none
  }
  .form-control[disabled],
  .form-control[readonly],
  fieldset[disabled] .form-control {
    opacity: 0.6;
    background-color: #fff;
    pointer-events: none
  }

  .input-group-btn button {
    min-height: 40px
  }

  .disabled-button {
    display: none
  }

  .form-group__message {
    color: red;
    font-weight: 400;
    word-spacing: 1px;
    font-size: 90%
  }
</style>
