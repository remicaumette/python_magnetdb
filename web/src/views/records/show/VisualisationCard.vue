<template>
  <Card>
    <template #header>
      Visualize
    </template>

    <Alert v-if="error" class="alert alert-danger mb-6" :error="error"/>

    <Form @submit="submit">
      <div class="flex items-center space-x-4">
        <div class="w-1/3">
          <FormField
              label="X Axis"
              name="x"
              :component="FormSelect"
              :options="columnOptions"
          />
        </div>
        <div class="w-1/3">
          <FormField
              label="Y Axis"
              name="y"
              :component="FormSelect"
              :options="columnOptions"
          />
        </div>
      </div>
      <div class="flex items-center space-x-4">
        <Button type="submit" class="btn btn-primary btn-small">
          Update
        </Button>
        <Button class="btn btn-default btn-small" @click="chart.resetZoom()">
          Reset zoom
        </Button>
      </div>
    </Form>

    <canvas ref="chart"></canvas>
  </Card>
</template>

<script>
import { Chart, registerables } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import Alert from "@/components/Alert";
import Card from "@/components/Card";
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormSelect from "@/components/FormSelect";
import * as recordService from '@/services/recordService'

Chart.register(...registerables, zoomPlugin)

export default {
  name: 'VisualisationCard',
  props: ['recordId'],
  components: {
    Form,
    FormField,
    Alert,
    Card,
  },
  data() {
    return {
      FormSelect,
      error: null,
      columnOptions: [],
      xField: 't',
      yField: 'Q',
      chart: null,
    }
  },
  methods: {
    submit(values) {
      this.xField = values.x.value
      this.yField = values.y.value
      return this.fetch()
    },
    async fetch() {
      return recordService.visualize({ id: this.recordId, x: this.xField, y: this.yField })
        .then((data) => {
          this.chart.data.labels = Object.keys(data.result)
          this.chart.data.datasets[0].label = this.yField
          this.chart.data.datasets[0].data = Object.values(data.result)
          this.chart.update()
          this.columnOptions = data.columns.map(name => ({ name, value: name }))
        })
        .catch((error) => {
          this.error = error
        })
    },
  },
  async mounted() {
    this.chart = new Chart(this.$refs.chart, {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          {
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [],
          }
        ]
      },
      options: {
        plugins: {
          zoom: {
            pan: {
              enabled: true,
              mode: 'x',
              modifierKey: 'ctrl',
            },
            zoom: {
              drag: {
                enabled: true
              },
              mode: 'x',
            },
          }
        },
      },
    })

    await this.fetch()
  }
}
</script>
