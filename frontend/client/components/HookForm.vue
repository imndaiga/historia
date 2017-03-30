<template id="app-form">
  <form v-on:submit.prevent="submitForm" :class="{'form-inline': form_is_inline}">
    <div v-for="field in form" v-if="$v.form_object[field.field_name] != null" :class="['form-group', field.classes, {'has-error': $v.form_object[field.field_name].$error}]">
      <div v-if="field.type == 'hidden-input'" style="display: none;" :key="field.id">
        <label>{{ field.label }}</label>
        <input type="text" :name="field.field_name" :value="field.placeholder" readonly>
      </div>
      <label v-else>{{ field.label }}</label>
      <span class="form-group__message" v-if="Object.keys($v.form_object[field.field_name].value).indexOf('required') != -1"> *</span>
      <div v-if="['alpha-input', 'email-input'].indexOf(field.type) != -1" :class="{'input-group': field.value != undefined}">
        <input type="text" class="form-control" :name="field.field_name" v-model.trim="form_object[field.field_name].value" :placeholder="field.placeholder" v-on:input="$v.form_object[field.field_name].value.$touch()" :key="field.id" :readonly="field.value != undefined && !form_object[field.field_name].activated">
        <div v-if="field.value != undefined" class="input-group-btn">
          <button type="button" class="btn btn-warning" v-on:click="activateField(field.field_name)">
            Change
          </button>
        </div>
      </div>
      <div v-else-if="field.type == 'pikaday-input'" class="input-group">
        <input type="text" class="form-control" :name="field.field_name" :ref="field.field_name"  v-model.trim="form_object[field.field_name].value" v-on:input="$v.form_object[field.field_name].value.$touch()" readonly :key="field.id">
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
        <multiselect :options="field.multiselect_options" :placeholder="field.placeholder" deselect-label="Remove" select-label="Select" v-model="form_object[field.field_name].value" v-on:input="$v.form_object[field.field_name].value.$touch()" :key="field.id" :disabled="field.value != undefined && !form_object[field.field_name].activated" :select-label="field.SelectLabel" :deselect-label="field.DeselectLabel"></multiselect>
        <div v-if="field.value != undefined" class="input-group-btn">
          <button type="button" class="btn btn-warning" v-on:click="activateField(field.field_name)">
          Change
          </button>
        </div>
      </div>
      <div v-else-if="field.type == 'search-input'" :class="{'input-group': field.value != undefined}">
        <multiselect :options="form_object[field.field_name].options" :placeholder="field.placeholder" :loading="form_object[field.field_name].loading" :options-limit="10" :searchable="true" :internal-search="false" v-on:search-change="asyncFind(field.field_name, $event)" v-model="form_object[field.field_name].value" v-on:input="$v.form_object[field.field_name].value.$touch()" :key="field.id" :disabled="field.value != undefined && !form_object[field.field_name].activated" :select-label="field.SelectLabel" :deselect-label="field.DeselectLabel">
          <span slot="noResult">Oops! No person found under that name.</span>
        </multiselect>
        <div v-if="field.value != undefined" class="input-group-btn">
          <button type="button" class="btn btn-warning" v-on:click="activateField(field.field_name)">
            Change
          </button>
        </div>
      </div>
      <!-- <pre v-if="!!$v.form_object[field.field_name].value">{{$v.form_object[field.field_name].value}}</pre> -->
      <span class="form-group__message" v-if="!$v.form_object[field.field_name].value.required && Object.keys($v.form_object[field.field_name].value).indexOf('required') != -1 && $v.form_object[field.field_name].value.$dirty">{{ field.label }} is required</span>
      <span class="form-group__message" v-else-if="!$v.form_object[field.field_name].value.alpha && Object.keys($v.form_object[field.field_name].value).indexOf('alpha') != -1 && $v.form_object[field.field_name].value.$dirty">{{ field.label }} is not valid</span>
      <span class="form-group__message" v-else-if="!$v.form_object[field.field_name].value.email && Object.keys($v.form_object[field.field_name].value).indexOf('email') != -1 && $v.form_object[field.field_name].value.$dirty">Invalid email address</span>
    </div>
    <div v-for="field in form" v-if="field.type == 'submit-button'" class="form-group">
      <button type="submit" :class="field.button_class">{{ field.button_message }}</button>
    </div>
  </form>
</template>

<script>
</script>

<style>
</style>