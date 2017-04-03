<template>
  <form v-on:submit.prevent="submitForm" :class="{'form-inline': form_is_inline}">
    <div v-for="field in form" v-if="validateField(field.field_name).exists" :class="['form-group', field.classes, {'has-error': validateField(field.field_name).has_error}]">
      <div v-if="field.type == 'hidden-input'" style="display: none;" :key="field.key">
        <label>{{ field.label }}</label>
        <input type="text" :name="field.field_name" :value="field.placeholder" readonly>
      </div>
      <label v-else>{{ field.label }}</label>
      <span class="form-group__message" v-if="validateField(field.field_name).is_required"> *</span>
      <div v-if="['alpha-input', 'email-input'].indexOf(field.type) != -1" :class="{'input-group': field.value != undefined}">
        <input type="text" class="form-control" :name="field.field_name" v-model.trim="form_object[field.field_name].value" :placeholder="field.placeholder" v-on:input="touchField(field.field_name)" :key="field.key" :readonly="field.value != undefined && !form_object[field.field_name].activated">
        <div v-if="field.value != undefined" class="input-group-btn">
          <button type="button" class="btn btn-warning" v-on:click="activateField(field.field_name)">
            Change
          </button>
        </div>
      </div>
      <div v-if="field.type == 'password-input'" :class="{'input-group': field.value != undefined}">
        <input type="password" class="form-control" :name="field.field_name" v-model.trim="form_object[field.field_name].value" :placeholder="field.placeholder" v-on:input="touchField(field.field_name)" :key="field.key" :readonly="field.value != undefined && !form_object[field.field_name].activated">
        <div v-if="field.value != undefined" class="input-group-btn">
          <button type="button" class="btn btn-warning" v-on:click="activateField(field.field_name)">
            Change
          </button>
        </div>
      </div>
      <div v-else-if="field.type == 'pikaday-input'" class="input-group">
        <input type="text" class="form-control" :name="field.field_name" :placeholder="field.placeholder" :ref="field.field_name"  v-model.trim="form_object[field.field_name].value" v-on:input="touchField(field.field_name)" readonly :key="field.key">
        <div class="input-group-btn">
          <button type="button" :ref="field.field_name+'-btn'" :class="['btn', 'btn-default', {'disabled-button': field.value != undefined && !form_object[field.field_name].activated}]">
            <i class="fa fa-calendar fa-lg"></i>
          </button>
          <button v-if="field.value != undefined" type="button" class="btn btn-warning" v-on:click="activateField(field.field_name)">
            Change
          </button>
        </div>
      </div>
      <div v-else-if="field.type == 'multiselect-input'" :class="{'input-group': field.value != undefined}">
        <multiselect :options="field.multiselect_options" :placeholder="field.placeholder" deselect-label="Remove" select-label="Select" v-model="form_object[field.field_name].value" v-on:input="touchField(field.field_name)" :key="field.id" :disabled="field.value != undefined && !form_object[field.field_name].activated" :select-label="field.SelectLabel" :deselect-label="field.DeselectLabel"></multiselect>
        <div v-if="field.value != undefined" class="input-group-btn">
          <button type="button" class="btn btn-warning" v-on:click="activateField(field.field_name)">
          Change
          </button>
        </div>
      </div>
      <div v-else-if="field.type == 'search-input'" :class="{'input-group': field.value != undefined}">
        <multiselect :options="form_object[field.field_name].options" :placeholder="field.placeholder" :loading="form_object[field.field_name].loading" :options-limit="10" :searchable="true" :internal-search="false" v-on:search-change="asyncFind(field.field_name, $event)" v-model="form_object[field.field_name].value" v-on:input="touchField(field.field_name)" :key="field.id" :disabled="field.value != undefined && !form_object[field.field_name].activated" :select-label="field.SelectLabel" :deselect-label="field.DeselectLabel">
          <span slot="noResult">Oops! Person not found.</span>
        </multiselect>
        <div v-if="field.value != undefined" class="input-group-btn">
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
    <div v-for="field in form" v-if="field.type == 'submit-button'" class="form-group">
      <button type="submit" :class="field.button_class">{{ field.button_message }}</button>
    </div>
  </form>
</template>

<script>
  var isBrowser = false
  if (process.browser) {
    var Pikaday = require('pikaday')
    var Multiselect = require('vue-multiselect').default
    isBrowser = true
  }
  export default {
    components: {
      multiselect: Multiselect
    },
    props: {
      form: {
        type: Array,
        required: true
      },
      submit_resource: {
        type: String,
        required: true
      },
      search_resource: {
        type: String,
        required: true
      },
      form_is_inline: {
        type: Boolean,
        required: true
      }
    },
    data: function () {
      return {
        form_object: this.createFormObject()
      }
    },
    validations: function () {
      var validationsDict = {}
      validationsDict['form_object'] = {}
      for (var index in this.form) {
        var key = this.form[index].field_name
        if (key !== undefined) {
          validationsDict.form_object[key] = {}
          validationsDict.form_object[key].value = {}
          if (Object.keys(this.form[index]).indexOf('validators') !== -1) {
            var validators = this.form[index].validators
            validationsDict.form_object[key].value = validators
          }
        }
      }
      return validationsDict
    },
    methods: {
      submitForm: function () {
        var self = this
        if (!this.$v.$invalid) {
          var formData = {}
          for (var field in this.form_object) {
            formData[field] = this.form_object[field].value
          }
          // Send form data to submit resource
          if (this.submit_resource === 'login') {
            var unauthorisedAlert = {
              message: 'Ooops! Please try again',
              type: 'alert-danger',
              dismissable: true,
              duration: 0
            }
            var authorisedAlert = {
              message: 'Yay! Welcome',
              type: 'alert-success',
              dismissable: true,
              duration: 0
            }
            this.$nuxt.$store.dispatch('login', formData)
            .then(function (response) {
              if (response.status === 200) {
                self.$nuxt.$store.dispatch('alert', authorisedAlert)
                self.$nuxt.$router.push('/user/home')
              } else {
                self.$nuxt.$store.dispatch('alert', unauthorisedAlert)
              }
            })
          }
        } else {
          this.$v.$touch()
        }
      },
      asyncFind: function (fieldName, value) {
        this.form_object[fieldName].loading = true
        // Perform full text search here
      },
      createFormObject: function () {
        var formObject = {}
        for (var index in this.form) {
          var key = this.form[index].field_name
          if (this.form[index].type !== 'submit-button') {
            formObject[key] = {}
            if (this.form[index].type === 'search-input') {
              formObject[key]['loading'] = false
              formObject[key]['options'] = []
            }
            if (Object.keys(this.form[index]).indexOf('value') !== -1) {
              formObject[key]['value'] = this.form[index].value
            } else {
              formObject[key]['value'] = ''
            }
            formObject[key]['activated'] = false
          }
        }
        return formObject
      },
      activateField: function (fieldName) {
        this.form_object[fieldName].activated = true
        this.$nuxt.$emit('form-field-activated')
      },
      validateField: function (fieldName) {
        // Replace with better implementation, creates hydration errors
        var validation = {}
        if (isBrowser && fieldName) {
          validation.exists = this.$v.form_object[fieldName] !== null
          validation.has_error = this.$v.form_object[fieldName].$error
          validation.is_dirty = this.$v.form_object[fieldName].value.$dirty
          validation.is_required = Object.keys(this.$v.form_object[fieldName].value).indexOf('required') !== -1
          validation.is_alpha = Object.keys(this.$v.form_object[fieldName].value).indexOf('alpha') !== -1
          validation.is_email = Object.keys(this.$v.form_object[fieldName].value).indexOf('email') !== -1
          validation.failed_required = !this.$v.form_object[fieldName].value.required && validation.is_required && validation.is_dirty
          validation.failed_alpha = !this.$v.form_object[fieldName].value.alpha && validation.is_alpha && validation.is_dirty
          validation.failed_email = !this.$v.form_object[fieldName].value.email && validation.is_email && validation.is_dirty
        }
        return validation
      },
      touchField: function (fieldName) {
        // Replace with better implementation, creates hydration errors
        if (isBrowser && fieldName) {
          this.$v.form_object[fieldName].value.$touch()
        }
      }
    },
    computed: {
      pikaday_Hooks: function () {
        if (isBrowser) {
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
        return null
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
          }
        })
      }
    }
  }
</script>

<style>
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
  .form-control[disabled], .form-control[readonly], fieldset[disabled] .form-control {
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
