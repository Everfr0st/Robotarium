<template>
  <div>
    <v-row v-if="connected" class="tacometers">
      <v-col sm="4">
        <highcharts :options="chartOptionsLeft"></highcharts>
      </v-col>
      <v-col sm="4">
        <highcharts :options="chartOptionsRight"></highcharts>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { Chart } from "highcharts-vue";
import Highcharts from "highcharts";
import hcMore from "highcharts/highcharts-more";
import ROSLIB from "roslib";

hcMore(Highcharts);

export default {
  name: "Tacometer",
  components: {
    highcharts: Chart,
  },
  computed: {},
  mounted() {
  
    this.$root.$on("angSpeeds", (data) => {
      if (data) {
        this.chartOptionsLeft.series[0].data = [data.vel_left];
        this.chartOptionsRight.series[0].data = [data.vel_right];
        this.connected = data;
      }
    });
  },
  methods: {},
  data() {
    return {
      chartOptionsLeft: {
        chart: {
          type: "gauge",
          plotBackgroundColor: null,
          plotBackgroundImage: null,
          plotBorderWidth: 0,
          plotShadow: false,
        },

        title: {
          text: "Velocidad ang. llanta izquierda",
        },

        pane: {
          startAngle: -150,
          endAngle: 150,
          background: [
            {
              backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                  [0, "#FFF"],
                  [1, "#333"],
                ],
              },
              borderWidth: 0,
              outerRadius: "109%",
            },
            {
              backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                  [0, "#333"],
                  [1, "#FFF"],
                ],
              },
              borderWidth: 1,
              outerRadius: "107%",
            },
            {
              // default background
            },
            {
              backgroundColor: "#DDD",
              borderWidth: 0,
              outerRadius: "105%",
              innerRadius: "103%",
            },
          ],
        },

        // the value axis
        yAxis: {
          min: -0.5,
          max: 0.5,

          minorTickInterval: "auto",
          minorTickWidth: 1,
          minorTickLength: 10,
          minorTickPosition: "inside",
          minorTickColor: "#666",

          tickPixelInterval: 30,
          tickWidth: 2,
          tickPosition: "inside",
          tickLength: 10,
          tickColor: "#666",
          labels: {
            step: 2,
            rotation: "auto",
          },
          title: {
            text: "rad/seg",
          },
          plotBands: [
            {
              from: 0.3,
              to: 0.5,
              color: "#55BF3B", // green
            },
            {
              from: 0,
              to: 0.3,
              color: "#DDDF0D", // yellow
            },
            {
              from: -0.5,
              to: 0,
              color: "#DF5353", // red
            },
          ],
        },

        series: [
          {
            name: "Velocidad",
            data: [0],
            tooltip: {
              valueSuffix: " rad/seg",
            },
          },
        ],
      },
      chartOptionsRight: {
        chart: {
          type: "gauge",
          plotBackgroundColor: null,
          plotBackgroundImage: null,
          plotBorderWidth: 0,
          plotShadow: false,
        },

        title: {
          text: "Velocidad ang. llanta derecha",
        },

        pane: {
          startAngle: -150,
          endAngle: 150,
          background: [
            {
              backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                  [0, "#FFF"],
                  [1, "#333"],
                ],
              },
              borderWidth: 0,
              outerRadius: "109%",
            },
            {
              backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                  [0, "#333"],
                  [1, "#FFF"],
                ],
              },
              borderWidth: 1,
              outerRadius: "107%",
            },
            {
              // default background
            },
            {
              backgroundColor: "#DDD",
              borderWidth: 0,
              outerRadius: "105%",
              innerRadius: "103%",
            },
          ],
        },

        // the value axis
        yAxis: {
          min: -0.5,
          max: 0.5,
          minorTickInterval: "auto",
          minorTickWidth: 1,
          minorTickLength: 10,
          minorTickPosition: "inside",
          minorTickColor: "#666",
          tickPixelInterval: 30,
          tickWidth: 2,
          tickPosition: "inside",
          tickLength: 10,
          tickColor: "#666",
          labels: {
            step: 2,
            rotation: "auto",
          },
          title: {
            text: "rad/seg",
          },
          plotBands: [
            {
              from: 0.3,
              to: 0.5,
              color: "#55BF3B", // green
            },
            {
              from: 0,
              to: 0.3,
              color: "#DDDF0D", // yellow
            },
            {
              from: -0.5,
              to: 0,
              color: "#DF5353", // red
            },
          ],
        },

        series: [
          {
            name: "Velocidad",
            data: [0],
            tooltip: {
              valueSuffix: " rad/seg",
            },
          },
        ],
      },
      snackbar: false,
      snackMsg: "",
      connected: false,
    };
  },
};
</script>
<style  scoped>
</style>
