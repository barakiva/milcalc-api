import {
  getTotalDaysIn2023,
  specialGrantCalculation,
  totalDaysInRange,
  isOneRangeMoreThan5Days,
  calculateDays,
} from '../calculator'

describe('Calculator', () => {
  describe('totalDaysInRange', () => {
    it('should return 0 if start date is after end date', () => {
      expect(
        totalDaysInRange(new Date('2021-01-02'), new Date('2020-01-01'))
      ).toBe(0)
    })

    it('should return 1 if start date is same as end date', () => {
      expect(
        totalDaysInRange(new Date('2021-01-01'), new Date('2021-01-01'))
      ).toBe(1)
    })

    it('should return correct number of days if start date is before end date', () => {
      expect(
        totalDaysInRange(new Date('2021-01-01'), new Date('2021-01-31'))
      ).toBe(31)
    })
  })

  describe('getTotalDaysIn2023', () => {
    it('should return 0 if date ranges not in 2023', () => {
      expect(
        getTotalDaysIn2023([
          {
            startDate: new Date('2021-01-01'),
            endDate: new Date('2021-01-31'),
          },
          {
            startDate: new Date('2024-01-01'),
            endDate: new Date('2024-01-31'),
          },
        ])
      ).toBe(0)
    })

    it('should return currect number of days in 2023', () => {
      expect(
        getTotalDaysIn2023([
          {
            startDate: new Date('2023-12-31'),
            endDate: new Date('2024-01-30'),
          },
        ])
      ).toBe(1)

      expect(
        getTotalDaysIn2023([
          {
            startDate: new Date('2023-01-01'),
            endDate: new Date('2023-01-31'),
          },
          {
            startDate: new Date('2023-02-01'),
            endDate: new Date('2023-02-28'),
          },
          {
            startDate: new Date('2023-12-31'),
            endDate: new Date('2024-12-01'),
          },
        ])
      ).toBe(60)
    })
  })

  describe('specialGrantCalculation', () => {
    it('should return correct number of days', () => {
      expect(specialGrantCalculation(0, 0, false)).toStrictEqual({
        totalDaysStraight: 0,
        totalAdditional: 0,
        totalSpecialDays: 0,
        totalExtended: 0,
      })
    })
    it('should calculate correctly for basic input', () => {
      expect(specialGrantCalculation(10, 5, false)).toEqual({
        totalDaysStraight: 0,
        totalSpecialDays: 0,
        totalExtended: 0,
        totalAdditional: 2820,
      })
    })
    it('should handle edge case of 14.5 total days', () => {
      expect(specialGrantCalculation(14, 0.5, true)).toEqual({
        totalDaysStraight: 266,
        totalSpecialDays: 0,
        totalExtended: 0,
        totalAdditional: 1410,
      })
    })
    it('should calculate correctly for days before 32', () => {
      expect(specialGrantCalculation(20, 10, true)).toEqual({
        totalDaysStraight: 266,
        totalSpecialDays: 0,
        totalExtended: 0,
        totalAdditional: 4230,
      })
    })

    it('should calculate zero for negative values', () => {
      expect(specialGrantCalculation(-5, -10, false)).toEqual({
        totalDaysStraight: 0,
        totalSpecialDays: 0,
        totalExtended: 0,
        totalAdditional: 0,
      })
    })

    it('should calculate correctly for 95 war days', () => {
      expect(specialGrantCalculation(0, 95, true)).toEqual({
        totalDaysStraight: 266,
        totalSpecialDays: 0,
        totalExtended: 8512,
        totalAdditional: 5640,
      })
    })
  })

  describe('isOneRangeMoreThan5Days', () => {
    it('should return false if no ranges', () => {
      expect(isOneRangeMoreThan5Days([])).toBe(false)
    })
    it('should return false if no range is more than 5 days', () => {
      expect(
        isOneRangeMoreThan5Days([
          {
            startDate: new Date('2021-01-01'),
            endDate: new Date('2021-01-04'),
          },
          {
            startDate: new Date('2021-01-06'),
            endDate: new Date('2021-01-09'),
          },
        ])
      ).toBe(false)
    })

    it('should return true if one range is more than 5 days', () => {
      expect(
        isOneRangeMoreThan5Days([
          {
            startDate: new Date('2021-01-01'),
            endDate: new Date('2021-01-04'),
          },
          {
            startDate: new Date('2021-01-06'),
            endDate: new Date('2021-01-11'),
          },
        ])
      ).toBe(true)
    })
  })

  describe('calculateDays', () => {
    it('should return 0 if no date ranges', () => {
      expect(calculateDays([])).toBe(0)
    })

    it('should return correct number of days for basic input', () => {
      expect(
        calculateDays([
          {
            startDate: new Date('2021-01-01'),
            endDate: new Date('2021-01-04'),
          },
          {
            startDate: new Date('2021-01-06'),
            endDate: new Date('2021-01-11'),
          },
        ])
      ).toBe(10)
    })

    it('should return correct number of days for basic input', () => {
      expect(
        calculateDays([
          {
            startDate: new Date('2023-10-07'),
            endDate: new Date('2024-01-09'),
          },
        ])
      ).toBe(95)
    })
  })
})
