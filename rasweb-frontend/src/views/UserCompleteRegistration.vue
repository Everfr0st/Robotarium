<template>
  <div>
    <v-card>
      <v-card-title>Define tu rol</v-card-title>
      <v-card-text>
        <form @submit.prevent="setUserRole">
          <v-select
            :rules="[rules.required]"
            label="Rol"
            v-model="role"
            :items="['Estudiante', 'Docente']"
            :readonly="userRole"
          ></v-select>
          <div v-if="role == 'Estudiante'">
            <v-text-field
              :rules="[rules.required]"
              v-model="career"
              label="Carrera"
            ></v-text-field>
            <v-select
              v-model="semester"
              :rules="[rules.required]"
              :items="semesters"
              label="Semestre"
            ></v-select>
          </div>
          <div v-else-if="role == 'Docente'">
            <v-text-field
              label="Departamento"
              :rules="[rules.required]"
              v-model="department"
            ></v-text-field>
            <p>Fecha de inicio</p>
            <v-date-picker
              :rules="[rules.required]"
              class="mx-auto"
              full-width
              v-model="dateStart"
            ></v-date-picker>
          </div>
          <v-btn
            @click="setUserRole"
            :loading="loading"
            color="primary darken-1"
            block
            >Guardar</v-btn
          >
        </form>
      </v-card-text>
    </v-card>
    <v-snackbar v-model="snackbar">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbar = false">
          cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
export default {
  name: "UserCompleteRegistration",
  data: () => ({
    role: "",
    career: "",
    semester: "",
    department: "",
    dateStart: "",
    apiDir: "/robotarium-api/v1.0/user-role/",
    userRole: false,
    semesters: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    rules: {
      required: (value) => !!value || "Obligatorio",
    },
    loading: false,
    message: "",
    snackbar: false,
  }),
  computed: {
    ...mapState(["domainBase", "selfUser", "authentication"]),
  },
  mounted() {
    this.getUserRole();
    this.setViewname("Rol");
  },
  
  methods: {
    ...mapMutations(["setViewname"]),
    getUserRole() {
      fetch(this.domainBase + this.apiDir, {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => {
          if (response.status == 200) {
            return response.json();
          } else {
            throw new Error();
          }
        })
        .then((response) => {
          if(!response.role) return 0;
          this.role = response.role;
          this.userRole = true
          if (response.role == "Estudiante") {
            this.career = response.career;
            this.semester = response.semester;
          } else if (response.role == "Docente") {
            this.department = response.department;
            this.dateStart = response.date_start;
          }
        })
        .catch((err) => console.error(err));
    },
    setUserRole() {
      this.loading = true;
      let formData = {};
      if (this.role == "Estudiante" && this.career && this.semester) {
        formData = {
          role: this.role,
          career: this.career,
          semester: this.semester,
        };
      } else if (this.role == "Docente" && this.department && this.dateStart) {
        formData = {
          role: this.role,
          department: this.department,
          date_start: this.dateStart,
        };
      } else {
        this.snackbar = true;
        this.message = "Debes ingresar toda la información";
        this.loading = false;
        return 0;
      }
      fetch(this.domainBase + this.apiDir, {
        method: "PUT",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      }).finally(() => {
        this.loading = false;
      });
    },
  },
};
</script>

<style>
</style>